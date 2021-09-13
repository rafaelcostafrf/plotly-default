# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np

from scipy import stats

from apps.plots import PlotBar, PlotHist
from apps.visions import gen_dict, SingleGraph, MultiGraphDropDown, SingleDropdown

from layouts import ml_layout

app = dash.Dash(__name__)
server = app.server

# Importando a database
df = pd.read_csv('database/dataset_2021-5-26-10-14.csv', sep='\t', encoding = 'utf-8')

# Removendo outliers do valor de pedido
df = df[(np.abs(stats.zscore(df['valor_total_pedido'])) < 0.08)]
df = df.sort_values(by='valor_total_pedido')

# Reconhecendo todos os valores únicos de tipo de sociedade
tipo_sociedade_unique = sorted(df['tipo_sociedade'].unique())
tipo_sociedade_dropdown = [{'label': x, 'value': x} for x in tipo_sociedade_unique]

# Plotando o histograma de compras
fig_total = PlotHist(
                x = df['valor_total_pedido'],
                color = df['default'],
                colors_values= ['#FFF4BD', '#85D2D0'],
                labels_dict={'x': 'Valor Total Pedidos', 'y': 'Quantidade', 'color': 'Default'},
                range_x = [0, 20000],
                nbins = 2000
                )


# Histograma de valores de pedidos separados por default 1
df_default = df.where(df['default']==1)

# Histograma de valores de pedidos separados por default 0
df_n_default = df.where(df['default']==0)

# Análise de default por tipo de sociedade
d_tipo = pd.DataFrame({'default 0': df_n_default['tipo_sociedade'].value_counts(), 
                        'valor recebido': df_n_default.groupby('tipo_sociedade')['valor_total_pedido'].sum(), 
                        'default 1': df_default['tipo_sociedade'].value_counts(),
                        'valor default': df_default.groupby('tipo_sociedade')['valor_total_pedido'].sum(),})

# Organizando os valores para apresentação
d_tipo = d_tipo.sort_values(by='valor recebido', ascending=False)

# Plot em barras do tipo de sociedade e sua proporção de valor recebido e valor default
fig_tipo = PlotBar(
                df=d_tipo,
                y=['valor recebido', 'valor default'],
                colors_values=['#FFF4BD', '#85D2D0'],
                range_x = [-1, 6])


# Dicionário para o multigraph dropdown
sociedade_multi_dict = [
    gen_dict(
        title='Valor Total Pedidos', 
        graph_name='tipo_sociedade_graph',
        dropdown_name='tipo_sociedade_dropdown',
        dropdown_options=tipo_sociedade_dropdown),

    gen_dict(
        title='Análise Default Três Meses', 
        graph_name='grafico_default_3_meses',
        dropdown_name='default_dropdown',
        dropdown_options=tipo_sociedade_dropdown),
    
]

# Reconhecendo todos os valores únicos de ano
year_unique = sorted(df['year'].unique())
year_dropdown = [{'label': x, 'value': x} for x in year_unique]
year_dict = gen_dict(
        title='Valor de Pedidos por Ano', 
        graph_name='ano_valor_graph',
        dropdown_name='year_dropdown',
        dropdown_options=year_dropdown)


# Layout do app
app.layout = html.Div(children=[

    html.Div(children=[
        html.H1(
        children='Análise de Default'),
    ], 
    style={'padding': '1px'},
    className='divBorder'),

    dcc.Tabs([
        
        dcc.Tab(label='Análise Tabular', children=[
            html.Div(children=[
                *SingleGraph('Valor Total de Pedidos', fig_total),

                *SingleGraph('Valor Total por Tipo de Sociedade', fig_tipo),

                *MultiGraphDropDown('Análise Tipo de Sociedade', sociedade_multi_dict),

                *SingleDropdown(year_dict),
            ], className='divBorder')
        ]),

        dcc.Tab(label='Análise Machine Learning', children=[
            *ml_layout,
        ]),
    ])
  ], 
  style={'padding': '10px'}, 
  className='divBorderLower')

