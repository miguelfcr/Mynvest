from services.webservice import Webservice

class WebFundamentus(Webservice):

	def __init__(self):
		super(WebFundamentus, self).__init__("https://www.fundamentus.com.br/")

	def get_ativo_table_list(self, papel):
		papel = self._getresult(self.link_base + "detalhes.php?papel=%s" % papel)
		return self._gettablelist(papel)

	def get_ativos_table(self):
		ativo_list = self._getresult(self.link_base + "detalhes.php?papel=")
		return self._gettable(ativo_list)
