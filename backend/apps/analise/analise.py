import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from pandas_datareader import data as wb
from pandas_datareader._utils import RemoteDataError
from repos.mongo import MongoRepo

class Analise:
    def __init__(self, start, end=datetime.today()):
        self.MR = MongoRepo()
        self.inicio = start.strftime("%Y-%m-%d")
        self.fim = end.strftime("%Y-%m-%d")

        self.close = pd.DataFrame()
        self.open = pd.DataFrame() 
        self.high = pd.DataFrame() 
        self.low =  pd.DataFrame()

    def get_ativos_where(self, query_dict, limit=9999):
        ativo_list = self.MR.select(query_dict, limit)

        for ativo_dict in ativo_list:
            try:
                price = wb.DataReader(ativo_dict['acao'] + ".SA" , data_source='yahoo', start=self.inicio, end=self.fim)
                self.open[ativo_dict['acao']] = price['Open'][~price['Open'].index.duplicated()] 
                self.close[ativo_dict['acao']] = price['Close'][~price['Close'].index.duplicated()] 
                self.high[ativo_dict['acao']] = price['High'][~price['High'].index.duplicated()] 
                self.low[ativo_dict['acao']] = price['Low'][~price['Low'].index.duplicated()] 

            except RemoteDataError:
                print ("Erro RemoteDataError ativo %s" % ativo_dict['acao'])

    def plot_grafico(self, x_label, y_label, atributo, normaliza=0):
        obj = eval("self.%s" % atributo)
        if normaliza:
            (obj/obj.iloc[0]*100).plot(figsize=(15,5))
        else:
            obj.plot(figsize=(15,5))

        plt.title("Grafico do {}".format(atributo))
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.show()

if __name__ == "__main__":
    A = Analise(datetime.strptime('2019-10-12', '%Y-%m-%d'), datetime.today())
    query_dict = {'cotacao': {"$lt": 8.0}}
    A.get_ativos_where(query_dict, 5)
    A.plot_grafico('data', 'valor', "close", 0)
