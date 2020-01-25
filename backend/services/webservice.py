import pandas as pd

from urllib.request import FancyURLopener
from bs4 import BeautifulSoup

class AppURLopener(FancyURLopener):
	version = "Mozilla/5.0"

class Webservice(object):

	def __init__(self, link_base):
		self.link_base = link_base

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

	def _getresult(self, link):
		result = None

		try:
			html = AppURLopener().open(link)
			result = BeautifulSoup(html.read(),"html5lib")
		except Exception as e:
			print('um erro ocorreu.', e)

		return result

