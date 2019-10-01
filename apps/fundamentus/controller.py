import traceback
import pandas as pd
from datetime import datetime
from pprint import pprint

from apps.fundamentus.webservice import WebFundamentus as WF
from apps.fundamentus.model import Controll, Ativo, Balanco, Demonstrativo, Indicadores
from apps.fundamentus.Exceptions import (BalancoException, AtivoFundamentusException, 
										CotacaoException, AtualizacaoException)

class Controller:
	def __init__(self):
		self.Controll = Controll()

	def atualiza_lista_ativos(self):
		ativos_list = WF().getativolist().rename(columns={"Papel": "acao"}).to_dict(orient='records')

		for ativo_dict in ativos_list:
			try:
				print("Inserindo dados do ativo:  %s" % ativo_dict['acao'])
				self.atualiza_ativo(ativo_dict['acao'])
			except (BalancoException, CotacaoException, AtivoFundamentusException, 
					AtualizacaoException) as b:
				print(b)
			except Exception as e:
				print(traceback.format_exc())
				return

	def atualiza_ativo(self, papel):
		ObjAtivo = self._get_ativo(papel)
		self.Controll.insert([ObjAtivo])

	def _get_ativo(self, papel):
		ObjAtivo = self.Controll.get_ativo(papel)

		if ObjAtivo.data_ultima_atualizacao == datetime.today().date():
			raise AtualizacaoException('Este ativo já foi atualizado na data de hoje')

		table_list = WF().getativo(papel)

		if len(table_list) < 5:
			raise AtivoFundamentusException('Ativo com numero de tables menor que 5')

		ativo_dict = self._prepara_cabecalho(table_list[0], table_list[1])
		ativo_dict['indicadores'] = [self._prepara_indicadores(table_list[2])]
		ativo_dict['balanco'] = [self._prepara_balanco(table_list[3])]
		ativo_dict['demonstrativo'] = [self._prepara_demonstrativo(table_list[4])]
		ativo_dict['data_ultima_atualizacao'] = datetime.today().date()
		
		# GAMBIARRA MODE ON
		for key, value in ativo_dict.items():
			ObjAtivo.__setattr__(key, value)
		# GAMBIARRA MODE OFF

		return ObjAtivo

	def _formata_campo(self, data, campo=''):
		ignore_list = ['acao', 'nome_empresa', 'setor', 'subsetor']
		try:
			newdata = data

			if campo in ignore_list:
				return newdata

			if data == '-':
				newdata = 0.0
			elif type(data) == str and data.strip() == '':
				newdata = ''
			elif type(data) == int or type(data) == float:
				newdata = data
			elif data.count('.') and data.replace('.','').isnumeric():
				newdata = float(data.replace('.',''))
			elif data.count('.') and data.count('-') and not data.count('%'):
				newdata = float(data.replace('.',''))
			elif data.count(',') and data.count('%'):
				newdata = float(data.replace('.','').replace(',','.').replace('%',''))
			elif data.count('/'):
				newdata = data  # Funciona sem formatar a data '-'
			elif data.isnumeric():
				newdata = float(data) / 100
		except Exception as e:
			print("Erro no campo: %s, valor: %s" % (campo, data))
			raise e

		return newdata

	def _prepara_cabecalho(self, cab0, cab1):
		cabecalho_dict = cab0[1].rename(index={0:'acao', 2:'nome_empresa', 3:'setor', 4:'subsetor'}).to_dict()
		cabecalho_dict.update(cab0[3].rename(index={0:'cotacao', 1:'data_ultima_cotacao'}).to_dict())
		cabecalho_dict.update(cab1[1].rename(index={0:'valor_mercado', 1:'valor_firma'}).to_dict())
		cabecalho_dict.update(cab1[3].rename(index={0:'data_ultimo_balanco', 1:'numero_acoes'}).to_dict())

		if not cabecalho_dict['data_ultima_cotacao'] or cabecalho_dict['data_ultima_cotacao'] == '-':
			raise CotacaoException('Data da última cotação inválida')

		if not cabecalho_dict['data_ultimo_balanco'] or cabecalho_dict['data_ultimo_balanco'] == '-':
			raise BalancoException('Data do último balanço inválido')
		
		# Valida a data do balanço
		dt_split = cabecalho_dict['data_ultimo_balanco'].split('/')
		new_dt_balanco = datetime(int(dt_split[2]), int(dt_split[1]), int(dt_split[0]))
		if (datetime.now() - new_dt_balanco).days > 365:
			raise BalancoException('Balanço com mais de 365 dias.')

		# Valida a data da cotação
		dt_split = cabecalho_dict['data_ultima_cotacao'].split('/')
		new_dt_cotacao = datetime(int(dt_split[2]), int(dt_split[1]), int(dt_split[0]))
		if (datetime.now() - new_dt_balanco).days > 5:
			raise CotacaoException('Cotação com mais de 5 dias.')

		return {k: self._formata_campo(v, k) for (k,v) in cabecalho_dict.items() if type(k) == str}

	def _prepara_balanco(self, bal):
		balanco_dict = bal[1].rename(index={1:'valor_ativo', 2:'disponibilidades', 3:'ativo_circulante'}).to_dict()
		balanco_dict.update(bal[3].rename(index={1:'divida_bruta', 2:'divida_liquida', 3:'patrimonio_liquido'}).to_dict())
		
		balanco_dict = {k: self._formata_campo(v, k) for (k,v) in balanco_dict.items() if type(k) == str}
		return Balanco(**balanco_dict)

	def _prepara_demonstrativo(self, dem):
		demonstrativo_dict = dem[1].rename(index={2:'receita_liquida_12', 3:'ebit_12', 4:'lucro_liquido_12'}).to_dict()
		demonstrativo_dict.update(dem[3].rename(index={2:'receita_liquida_3',  3:'ebit_3',  4:'lucro_liquido_3'}).to_dict())

		demonstrativo_dict = {k: self._formata_campo(v, k) for (k,v) in demonstrativo_dict.items() if type(k) == str}
		return Demonstrativo(**demonstrativo_dict)

	def _prepara_indicadores(self, ind):
		indicadores_dict = ind[3].rename(index={
									1: 'p_l', 7: 'p_ativ_circ_liq',
									2: 'p_vp', 8: 'div_yield', 
									3: 'p_ebit', 9: 'ev_ebit', 
									4: 'psr', 10: 'giro_ativos',
									5: 'p_ativos', 11: 'cres_rec5',
									6: 'p_cap_giro'}).to_dict()

		indicadores_dict.update(
								ind[5].rename(index={
									1: 'lpa', 6: 'ebit_ativo',
									2: 'vpa', 7: 'roic',
									3: 'marg_bruta', 8: 'roe',
									4: 'marg_ebit', 9: 'liquidez_corr',
									5: 'marg_liquida', 10: 'div_bruta_patrim',
								}).to_dict()
							)

		indicadores_dict = {k: self._formata_campo(v, k) for (k,v) in indicadores_dict.items() if type(k) == str}
		return Indicadores(**indicadores_dict)


if __name__ == "__main__":
	C = Controller()
	C.atualiza_lista_ativos()
