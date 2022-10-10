import pandas as pd
import json

#importando a base de dados
data22 = pd.read_csv('assets/dataeleicao22.csv')
data22.rename(columns={'NM_MUNICIPIO':'Cidade', 'QT_VOTOS':'Votos'}, inplace=True)

#gerando lista de nomes
nomes = list(data22['NM_VOTAVEL'].unique())
#gerando lista de cargos
cargos = list(data22['DS_CARGO'].unique())

#Pegando dados das cidades
with open("assets/cidades.json", "r") as read_cid:
    cidades = json.load(read_cid)