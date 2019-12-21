import sys

from apps.fundamentus.controller import Controller
from apps.fundamentus.model import Controll
from apps.fundamentus.analise import Analise

def run(option):
	
	if option == "makedb":
		Controll().recreate_database()
	elif option == "getativos":
		Controller().atualiza_lista_ativos()
	elif option == "analise":
		Analise().analise_todas()

if __name__ == "__main__":
	print(sys.argv)
	if "makedb" in sys.argv:
		run("makedb")
	
	elif "getativos" in sys.argv:
		run("getativos")

	elif "analise" in sys.argv:
		run("analise")
	
	else:
		print('makedb, getativos, analise')