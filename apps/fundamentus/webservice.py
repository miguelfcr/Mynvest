import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

class WebFundamentus(object):

	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, '_instance'):
			cls._instance = super(WebFundamentus, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		self.link_base = "https://www.fundamentus.com.br/"

	def _gettable(self, obj):
		table = self._gettablelist(obj)
		return table[0]

	def _gettablelist(self, obj):
		table_list = []
		tables = obj.findAll('table')

		if not tables:
			return table_list

		for table in tables:
			df = pd.read_html(str(table))
			table_list.append(df[0])

		return table_list

	def getativo(self, papel):
		papel = self._get(papel)
		return self._gettablelist(papel)

	def getativolist(self):
		ativo_list = self._get()
		return self._gettable(ativo_list)

	def getproventos(self, papel):
		link = self.link_base + "proventos.php?papel=%s&tipo=2" % papel
		res = self._getresult(link)
		return res

	def _get(self, papel=""):
		link = self.link_base + "detalhes.php?papel=%s" % papel
		res = self._getresult(link)
		return res

	def _getresult(self, link):
		result = None

		try:
			html = urlopen(link)
			result = BeautifulSoup(html.read(),"html5lib")
		except Exception as e:
			print('um erro ocorreu.')
			print(e)

		return result

