import pandas as pd

from apps.fundamentus.webservice import WebFundamentus as WF
from apps.fundamentus.model import Model

class Controller:
	def __init__(self):
		self.Model = Model()

	def atualizalistaativos(self):
		ativos_list = WF().getativolist().rename(columns={"Papel": "acao", "Nome Comercial": "nome"}).to_dict(orient='records')
		self.Model.inserelistaativos(ativos_list)
		
	def atualizaativo(self, papel):
		table_list = WF().getativo(papel)

		ativo_dict = self._preparacabecalho(table_list[0], table_list[1])
		ativo_dict['indicador_dict'] = self._preparaindicadores(1, table_list[2])
		ativo_dict['balanco_dict'] = self._preparabalanco(1, table_list[3])
		ativo_dict['demonstrativo_dict'] = self._preparademonstrativo(1, table_list[4])
		return ativo_dict

	def _formatacampo(self, data, campo=''):
		newdata = data
		try:
			if type(data) == int:
				newdata = data
			elif data.count('.') and data.replace('.','').isnumeric():
				newdata = float(data.replace('.',''))
			elif data.count('.') and data.count('-'):
				newdata = float(data.replace('.',''))
			elif data.count(',') and data.count('%'):
				newdata = float(data.replace(',','.').replace('%',''))
			elif data.count('/'):
				data = data.split('/')
				newdata = data[2] + '-' + data[1] + '-' + data[0]
			elif data.isnumeric():
				newdata = float(data) / 100
		except Exception as e:
			print(campo, e)

		return newdata

	def _preparacabecalho(self, cab0, cab1):
		cabecalho0 = cab0[1].rename(index={0:'acao', 3:'setor', 4:'subsetor'})
		cabecalho1 = cab0[3].rename(index={0:'cotacao', 1:'dtultcotacao'})
		cabecalho2 = cab1[1].rename(index={0:'vlmercado', 1:'vlfirma'})
		cabecalho3 = cab1[3].rename(index={0:'dtultbalanco', 1:'nracoes'})

		cabecalho_dict = cabecalho0.to_dict()
		cabecalho_dict.update(cabecalho1.to_dict())
		cabecalho_dict.update(cabecalho2.to_dict())
		cabecalho_dict.update(cabecalho3.to_dict())
		return {k: self._formatacampo(v, k) for (k,v) in cabecalho_dict.items() if type(k) == str}

		sql_update = """UPDATE ativo set 
					setor = '%(setor)s',
					subsetor = '%(subsetor)s',
					cotacao = %(cotacao)s,
					vlmercado = %(vlmercado)s,
					vlfirma = %(vlmercado)s,
					nracoes = %(nracoes)s,
					dtultcotacao = %(dtultcotacao)s,
					dtultbalanco = %(dtultbalanco)s 
					WHERE acao = '%(acao)s'""" % cabecalho_dict
		print(sql_update)

	def _preparabalanco(self, idativo, bal):
		balanco0 = bal[1].rename(index={1:'ativo', 2:'disponibilidades', 3:'ativocirculante'})
		balanco1 = bal[3].rename(index={1:'divbruta', 2:'divliquida', 3:'patrliq'})

		balanco_dict = {"idativo": idativo}
		balanco_dict.update(balanco0.to_dict())
		balanco_dict.update(balanco1.to_dict())
		return {k: self._formatacampo(v, k) for (k,v) in balanco_dict.items() if type(k) == str}

		sql_insert = """INSERT INTO balanco (idativo, ativo, disponibilidades, ativocirculante, divbruta, divliquida, patrliq)
						VALUES (%(idativo)s,
								%(ativo)s,
								%(disponibilidades)s,
								%(ativocirculante)s,
								%(divbruta)s,
								%(divliquida)s,
								%(patrliq)s)
					 """ % balanco_dict
		print(sql_insert)

	def _preparademonstrativo(self, idativo, dem):
		demonstrativo0 = dem[1].rename(index={2:'recliq12', 3:'ebit12', 4:'lucroliq12'})
		demonstrativo1 = dem[3].rename(index={2:'recliq3',  3:'ebit3',  4:'lucroliq3'})

		demonstrativo_dict = {"idativo": idativo}
		demonstrativo_dict.update(demonstrativo0.to_dict())
		demonstrativo_dict.update(demonstrativo1.to_dict())
		return {k: self._formatacampo(v, k) for (k,v) in demonstrativo_dict.items() if type(k) == str}

		sql_insert = """INSERT INTO demonstrativo (idativo, recliq12, ebit12, lucroliq12, recliq3, ebit3, lucroliq3)
						VALUES (%(idativo)s,
								%(recliq12)s,
								%(ebit12)s,
								%(lucroliq12)s,
								%(recliq3)s,
								%(ebit3)s,
								%(lucroliq3)s)
					 """ % demonstrativo_dict
		print(sql_insert)

	def _preparaindicadores(self, idativo, ind):
		indicador0 = ind[3].rename(index={
			1: 'p_l', 7: 'p_ativcircliq',
			2: 'p_vp', 8: 'divyield',  
			3: 'p_ebit', 9: 'ev_ebit', 
			4: 'psr', 10: 'giroativos',
			5: 'p_ativos', 11: 'cres_rec',
			6: 'p_capgiro',
		})
		indicador1 = ind[5].rename(index={
			1: 'lpa', 6: 'ebit_ativo',
			2: 'vpa', 7: 'roic',
			3: 'margbruta', 8: 'roe',
			4: 'margebit', 9: 'liquidezcorr',
			5: 'margliquida', 10: 'divbr_patrim',
		})

		indicador_dict = {"idativo": idativo}
		indicador_dict.update(indicador0.to_dict())
		indicador_dict.update(indicador1.to_dict())
		return {k: self._formatacampo(v, k) for (k,v) in indicador_dict.items() if type(k) == str}

		sql_insert = """INSERT INTO indicadores (idativo, p_l, p_vp, p_ebit, psr, p_ativos, p_capgiro, p_ativcircliq, 
												divyield, ev_ebit, giroativos, cres_rec, lpa, vpa, margbruta, margebit, 
												margliquida, ebit_ativo, roic, roe, liquidezcorr, divbr_patrim)
						VALUES (%(idativo)s,
								%(p_l)s,
								%(p_vp)s,
								%(p_ebit)s,
								%(psr)s,
								%(p_ativos)s,
								%(p_capgiro)s,
								%(p_ativcircliq)s,
								%(divyield)s,
								%(ev_ebit)s,
								%(giroativos)s,
								%(cres_rec)s,
								%(lpa)s,
								%(vpa)s,
								%(margbruta)s,
								%(margebit)s,
								%(margliquida)s,
								%(ebit_ativo)s,
								%(roic)s,
								%(roe)s,
								%(liquidezcorr)s,
								%(divbr_patrim)s)
					 """ % indicador_dict
		print(sql_insert)


if __name__ == "__main__":
	C = Controller()
	C.atualizalistaativos()