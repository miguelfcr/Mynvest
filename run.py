from apps.fundamentus.controller import Controller
from db.connection import DB

def run():
	db = DB()
	C = Controller()
	#C.get_dados_ativo('PETR4')
	#C.get_tabela_ativos()
	
if __name__ == "__main__":
	run()