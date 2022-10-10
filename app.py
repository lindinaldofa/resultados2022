from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash_auth
from _dados import *
from _funcoes import *

VALID_USERNAME_PASSWORD_PAIRS = {
    'naldo': 'Eleicoes2022'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
server = app.server

app.title = 'Painel de Resultados - Eleições 2022'

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

#Layout do Painel
app.layout = dbc.Container(
        children=[
                dbc.Row([
                    html.H1('Painel dos Resultado do primeiro turno das Eleições de 2022 em Alagoas', style={'textAlign': 'center', 'margin-top': '50px', 'margin-bottom': '50px'}),
                    
                    html.H5('Selecione o nome do candidato:', style={'textAlign': 'center', 'margin-bottom': '20px'}),
                    dcc.Dropdown(nomes, 'PAULO SURUAGY DO AMARAL DANTAS', id='sel_nome', style={'textAlign': 'center', 'margin-bottom': '40px'}),

                    html.H1('TOTAL DE VOTOS:', style={'textAlign': 'center', 'margin-top': '30px'}),
                    html.H2(id='total', style={'textAlign': 'center'}),

                    html.H1('Votos por Cidade', style={'textAlign': 'center', 'margin-top': '50px', 'margin-bottom': '30px'}),                            
                    dcc.Graph(id='pizza', style={'textAlign': 'center', 'margin-bottom': '30px'}),

                    dcc.Graph(
                        id='mapcid', style={'textAlign': 'center', 'margin-bottom': '30px'}), 
                    
                    html.Div(id='tabcidade', style={'textAlign': 'center', 'margin-bottom': '30px'}),
                    
                    html.H1('Votos por Local de Votação', style={'textAlign': 'center', 'margin-top': '50px', 'margin-bottom': '30px'}),                            
                    dcc.Graph(
                        id='maplocais', style={'textAlign': 'center', 'margin-bottom': '30px'}),            

                    html.Div(id='tablocais', style={'textAlign': 'center', 'margin-bottom': '30px'}),
                                    
                        ])
                ], fluid=True, )


@app.callback(
    [Output('total', 'children'),
    Output('pizza', 'figure'),
    Output('mapcid', 'figure'),
    Output('tabcidade', 'children'),
    Output('maplocais', 'figure'),
    Output('tablocais', 'children')],
    [Input('sel_nome', 'value')]
    )
def update_figure(candidato):
    datacand = data22.query("NM_VOTAVEL == '{0}'".format(candidato))
    total = '{:,}'.format(datacand['Votos'].sum())

    datacid = datacand.groupby(['Cidade'], as_index=False)['Votos'].sum()
    datacid['Porcentagem'] = round(datacid.Votos/datacid.Votos.sum()*100, 2)

    mapcid = px.choropleth_mapbox(datacid, geojson=cidades, locations='Cidade', featureidkey='properties.name', color='Votos',
                           color_continuous_scale=["red", "orange", "green"],
                           range_color=(0, escala(datacid)),
                           hover_name="Cidade",
                           height = 700, width = 1200,
                           mapbox_style="carto-positron",
                           zoom=7, center = {"lat": -9.7190576931341, "lon": -36.52170629244247},
                           opacity=0.5,
                           labels={'Votos':'Votos'}
                          )
    mapcid.update_layout(font_size=16, mapbox_accesstoken="pk.eyJ1IjoibGluZGluYWxkbyIsImEiOiJjbDFqenRma2IxbXN6M2VwM3ptc3l5OGUzIn0.dYrMp3TEvEBSsHAuv5sanA", mapbox_style = "mapbox://styles/lindinaldo/cl6od5yro000114p3vt7a6yii")


    figpie = px.pie(datacid, values='Votos', names='Cidade', hover_data=['Porcentagem'], hole=0.4)
    figpie.update_traces(hoverinfo='percent+label', textinfo='none')

    tabcidade = tabela_pag(datacid.sort_values("Votos", ascending=False))

    candlocal = pd.DataFrame(datacand.groupby(['Local', 'Endereco', 'LATITUDE', 'LONGITUDE', 'Zona'], as_index=False)['Votos'].sum())
    figmap = px.scatter_mapbox(candlocal, lat="LATITUDE", lon="LONGITUDE", size="Votos", hover_name="Local", size_max=40, zoom=7, opacity=0.5, color='Votos',
                  color_continuous_scale=["red", "orange", "green"], height = 700, width = 1200, labels={'Votos':'Votos'})
    figmap.update_layout(font_size=16, mapbox_accesstoken="pk.eyJ1IjoibGluZGluYWxkbyIsImEiOiJjbDFqenRma2IxbXN6M2VwM3ptc3l5OGUzIn0.dYrMp3TEvEBSsHAuv5sanA", mapbox_style = "mapbox://styles/lindinaldo/cl6od5yro000114p3vt7a6yii")
    

    dataloc = datacand.groupby(['Local'], as_index=False)['Votos'].sum()
    dataloc['Porcentagem'] = round(dataloc.Votos/dataloc.Votos.sum()*100, 2)

    tablocais = tabela_pag(dataloc.sort_values("Votos", ascending=False))


    return total,figpie,mapcid,tabcidade,figmap,tablocais




if __name__ == '__main__':
    app.run_server(debug=False)