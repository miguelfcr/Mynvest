import traceback
from pprint import pprint
from apps.fundamentus.model import Controll, Ativo

ANALISE_LIST = [
	# Max 1,5 ponto (total 15)
	"_calcula_ROE",
	"_calcula_MargLiq",
	"_calcula_PSR",
	"_calcula_DivYield",
	"_calcula_CresRec",
	"_calcula_LPA",
	"_calcula_PVP",
	"_calcula_ROIC",
	"_calcula_EvEbit",
	"_calcula_Valuation",
	# max 1 ponto (total 1)
	"_calcula_DividaLiq",
	# Retira 20 (total -40)
	"_calcula_PatrimLiq",
	"_calcula_LucroLiq12",
]

class Analise:
	def __init__(self):
		self.Controll = Controll()
	
	def analise_ativo(self, papel):
		ObjAtivo = self.Controll.get_ativo(papel)
		self._do_analize([ObjAtivo], fodase=True)

	def analise_todas(self):
		obj_ativo_list = self.Controll.get_ativos()
		self._do_analize(obj_ativo_list)

	def _do_analize(self, obj_ativo_list, fodase=False):
		result_list = []
		for ObjAtivo in obj_ativo_list:
			pontuacao = 0.0
			
			for metodo in ANALISE_LIST:
				pontuacao = eval("self.%s(ObjAtivo, pontuacao)" % metodo)

			if pontuacao > 8 or fodase:
				result_list.append({'acao':ObjAtivo.acao, 'pontuacao':pontuacao})

		result_list = sorted(result_list, key = lambda i: i['pontuacao'], reverse=True)
		self._print_result(result_list)

	def _print_result(self, result_list):
		print(' ACAO  | PONTUACAO')
		for result_dict in result_list:
			print("%6s | %s" % (result_dict['acao'], result_dict['pontuacao']))

	# VALIDADORES MAIOR MELHOR
	def _calcula_ROE(self, ObjAtivo, pontuacao):
		roe = ObjAtivo.indicadores.roe

		if roe >= 15:
			pontuacao += 1.5
		elif roe >= 10:
			pontuacao += 1.0
		elif roe >= 5:
			pontuacao += 0.5
		
		return pontuacao

	def _calcula_MargLiq(self, ObjAtivo, pontuacao):
		marg_liquida = ObjAtivo.indicadores.marg_liquida

		if marg_liquida >= 15:
			pontuacao += 1.5
		elif marg_liquida >= 10:
			pontuacao += 1.0
		elif marg_liquida >= 5:
			pontuacao += 0.5
		
		return pontuacao

	def _calcula_DivYield(self, ObjAtivo, pontuacao):
		div_yield = ObjAtivo.indicadores.div_yield

		if div_yield >= 10:
			pontuacao += 1.5
		elif div_yield >= 7:
			pontuacao += 1.0
		elif div_yield >= 4:
			pontuacao += 0.5
		
		return pontuacao

	def _calcula_CresRec(self, ObjAtivo, pontuacao):
		cres_rec5 = ObjAtivo.indicadores.cres_rec5

		if cres_rec5 >= 10:
			pontuacao += 1.5
		elif cres_rec5 >= 5:
			pontuacao += 1.0
		elif cres_rec5 >= 2:
			pontuacao += 0.5
		
		return pontuacao

	def _calcula_LPA(self, ObjAtivo, pontuacao):
		lpa = ObjAtivo.indicadores.lpa

		if lpa >= 2:
			pontuacao += 1.5
		elif lpa >= 1:
			pontuacao += 1.0
		elif lpa >= 0.5:
			pontuacao += 0.5
		
		return pontuacao

	def _calcula_ROIC(self, ObjAtivo, pontuacao):
		roic = ObjAtivo.indicadores.roic

		if roic >= 20:
			pontuacao += 1.5
		elif roic >= 10:
			pontuacao += 1.0
		elif roic >= 5:
			pontuacao += 0.5
		
		return pontuacao

	# VALIDADORES MENOR MELHOR
	def _calcula_PSR(self, ObjAtivo, pontuacao):
		psr = ObjAtivo.indicadores.psr

		if psr <= 0:
			return pontuacao

		if psr <= 1:
			pontuacao += 1.5
		elif psr <= 1.5:
			pontuacao += 1.0
		elif psr <= 2:
			pontuacao += 0.5
		
		return pontuacao

	def _calcula_PVP(self, ObjAtivo, pontuacao):
		p_vp = ObjAtivo.indicadores.p_vp

		if p_vp <= 0:
			return pontuacao

		if p_vp <= 1:
			pontuacao += 1.5
		elif p_vp <= 2:
			pontuacao += 1.0
		elif p_vp <= 3:
			pontuacao += 0.5
		
		return pontuacao

	def _calcula_EvEbit(self, ObjAtivo, pontuacao):
		ev_ebit = ObjAtivo.indicadores.ev_ebit

		if ev_ebit <= 0:
			return pontuacao

		if ev_ebit <= 10:
			pontuacao += 1.5
		elif ev_ebit <= 13:
			pontuacao += 1.0
		elif ev_ebit <= 16:
			pontuacao += 0.5
		
		return pontuacao

	# VALUATION
	def _calcula_Valuation(self, ObjAtivo, pontuacao):
		lpa = ObjAtivo.indicadores.lpa
		pl = ObjAtivo.indicadores.p_l
		cotacao = ObjAtivo.cotacao

		try:
			valuation = cotacao / (lpa*pl)
		except:
			return pontuacao

		if valuation <= 0.97:
			pontuacao += 1.05
		elif valuation <= 1.00:
			pontuacao += 1.0
		elif valuation <= 1.01:
			pontuacao += 0.5
		
		return pontuacao

	# DIVIDA
	def _calcula_DividaLiq(self, ObjAtivo, pontuacao):
		divida_liquida = ObjAtivo.balanco.divida_liquida

		if divida_liquida <= 0:
			pontuacao += 1.0
		
		return pontuacao
	
	# DESCONTOS
	def _calcula_PatrimLiq(self, ObjAtivo, pontuacao):
		patrimonio_liquido = ObjAtivo.balanco.patrimonio_liquido

		if patrimonio_liquido <= 0:
			pontuacao -= 20.0
		
		return pontuacao
	
	def _calcula_LucroLiq12(self, ObjAtivo, pontuacao):
		lucro_liquido_12 = ObjAtivo.demonstrativo.lucro_liquido_12
		if lucro_liquido_12 <= 0:
			pontuacao -= 20.0
		
		return pontuacao

if __name__ == "__main__":
	A = Analise()
	A.analise_todas()
	#A.analise_ativo('TAEE4')