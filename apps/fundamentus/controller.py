import pandas as pd

from apps.fundamentus.webservice import WebFundamentus as WF

class Controller:
	def __init__(self, db):
		self.db = db
	
	def gettabelaativos(self):
		tabela = WF().getativolist()
		print(tabela)

	def atualizalistaativos(self):
		ativos_list = WF().getativolist().rename(columns={"Papel": "acao", "Nome Comercial": "nome"}).to_dict(orient='records')
		for ativo_dict in ativos_list:
			sql_insert = "INSERT INTO ativo (acao, nomeempresa)"\
					 "VALUES (%(acao)s, %(nome)s)" % ativo_dict
			print(sql_insert)
		

if __name__ == "__main__":
	C = Controller(None)
	C.atualizalistaativos()
