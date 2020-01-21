from flask import Flask
from backend.apps.fundamentus.controller import Controller

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Tamo rodando galego<h1>"

@app.route('/atualiza')
def atualiza():
    return Controller().atualiza_lista_ativos()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)