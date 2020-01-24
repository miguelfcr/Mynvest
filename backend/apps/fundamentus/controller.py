import traceback
import logging as log

from datetime import datetime

from repos.mongo import MongoRepo
from apps.fundamentus.webservice.controller import WebServiceController
from Exceptions import (BalancoException, AtivoFundamentusException, CotacaoException)

class Controller:
	def __init__(self):
		self.WSC = WebServiceController()
		self.MongoRepo = MongoRepo()

	def atualiza_lista_ativos(self):
		ativos_list = self.WSC.get_papel_list()

		for ativo_dict in ativos_list:
			try:
				log.info('Atualizando ativo {}'.format(ativo_dict['acao']))
				self.atualiza_ativo(ativo_dict['acao'], ativo_dict['nome_empresa'])
			except (BalancoException, CotacaoException, AtivoFundamentusException) as b:
				log.warning("Ativo: {}, {}".format(ativo_dict['acao'], b))
			except Exception as e:
				log.error("Erro ao atualizar registros {} \n {}".format(e, traceback.format_exc()))

	def atualiza_ativo(self, papel, nome_empresa):
		ativo_dict = self.WSC.get_ativo_dict(papel)
		ativo_dict['nome_empresa'] = nome_empresa
		self._aplica_regra_validacao(papel, ativo_dict)
		self.MongoRepo.update_insert({'acao': papel}, ativo_dict)

	def _aplica_regra_validacao(self, papel, ativo_dict):
		if not ativo_dict['data_ultima_cotacao'] or ativo_dict['data_ultima_cotacao'] == '-':
			raise CotacaoException('Data da última cotação inválida')

		if not ativo_dict['data_ultimo_balanco'] or ativo_dict['data_ultimo_balanco'] == '-':
			raise BalancoException('Data do último balanço inválido')

		if (datetime.now() - ativo_dict['data_ultimo_balanco']).days > 365:
			raise BalancoException('Balanço com mais de 365 dias.')

		if (datetime.now() - ativo_dict['data_ultima_cotacao']).days > 5:
			raise CotacaoException('Cotação com mais de 5 dias.')

if __name__ == "__main__":
	C = Controller()
	C.atualiza_ativo('HBOR3', "HELLBOR")
	#C.atualiza_lista_ativos()
