import psycopg2
import psycopg2.extras


class DB(object):

	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, '_instance'):
			cls._instance = super(DB, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def getcur(self, name=""):
		cur = None
		try:
			cur = self.getcon().cursor(name=name, cursor_factory=psycopg2.extras.DictCursor)
		except (Exception, psycopg2.Error) as error:
			raise error

		return cur

	def getcon(self):
		connection = None
		try:
			connection = psycopg2.connect(user = "postgres",
										password = "postgres",
										host = "localhost",
										port = "5432",
										database = "mynvest")
		except (Exception, psycopg2.Error) as error :
			raise error

		return connection


	def getresult(self, sql):
		ret = []
		try:
			cur = self.getcur("select")
			cur.execute(sql)
			ret = cur.fetchall()
		except Exception as error:
			raise error
		finally:
			cur.close()

		return ret

	def getfirstresult(self, sql):
		ret = self.getresult(sql)
		return ret[0] if ret else []

	def execute(self, sql):
		con = self.getcur()
		cur = con.cursor()
		try:
			con.autocommit = True
			cur.execute(sql)
			cur.commit()
		except Exception as error:
			cur.rollback()
			raise error
		finally:
			cur.close()
			con.close()

if __name__ == "__main__":
	db = DB()
	print(db.getcur())
	print(db.getresult("select * from ativo"))