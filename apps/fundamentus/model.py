from db.connection import DB

class Model(object):

	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, '_instance'):
			cls._instance = super(Model, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		self.db = DB()

	def inserelistaativos(self, ativo_list):
		for ativo_dict in ativo_list:
			try:
				sql_insert = "INSERT INTO ativo (acao, nomeempresa)"\
						"VALUES (%(acao)s, %(nome)s)" % ativo_dict
				print(sql_insert)
			except Exception as e:
				print(e)

if __name__ == "__main__":
	M = Model()
