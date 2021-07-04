import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
from pandas_datareader import data as wb

from repos.mongo import MongoRepo

from requests.exceptions import ConnectionError
from pandas_datareader._utils import RemoteDataError
from urllib3.exceptions import ProtocolError

class Analise:
    def __init__(self, start=datetime.today(), end=datetime.today()):
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

            except (RemoteDataError, ConnectionError, ProtocolError):
                print ("Erro de conexao ativo %s" % ativo_dict['acao'])

    def plot_grafico(self, x_label, y_label, atributo, normaliza=0):
        obj = eval("self.%s" % atributo)
        if normaliza:
            (obj/obj.iloc[0]*100).plot(figsize=(15,5))
        else:
            obj.plot(figsize=(15,5))

        plt.title("Grafico do {}".format(atributo))
        plt.grid(True)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.show()

    def plot_correlation(self, subtitle):

        rets = self.close.pct_change()
        corr = rets.corr()
        
        plt.figure(figsize=(10, 10))
        plt.imshow(corr, cmap='RdYlGn', interpolation='none', aspect='auto')
        plt.colorbar()

        plt.xticks(range(len(corr)), corr.columns, rotation='vertical')
        plt.yticks(range(len(corr)), corr.columns)

        plt.suptitle(subtitle, fontsize=15, fontweight='bold')
        plt.show()




if __name__ == "__main__":
    A = Analise(datetime.strptime('2020-05-01', '%Y-%m-%d'), datetime.today())
    query_dict = {'cotacao': {"$lt": 8.0}}
    A.get_ativos_where(query_dict, 30)
    A.plot_grafico('data', 'valor', "close", 0)
    #A.plot_correlation("Correlação")
