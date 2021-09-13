import plotly.graph_objects as go

from dash.dependencies import Input, Output
from apps.plots import PlotHist, PlotBar
from apps.ml_regressor import default_prediction

from app import app, sociedade_multi_dict, df, year_dict

# Callbacks para os dropdowns
@app.callback(
    Output(sociedade_multi_dict[0]['graph_name'], 'figure'),
    Input(sociedade_multi_dict[0]['dropdown_name'], 'value'))
def update_graph(tipo_sociedade_name):
    fig = PlotHist(
                    x=df[df['tipo_sociedade']==tipo_sociedade_name].sort_values(by=['default'])['valor_total_pedido'], 
                    color=df[df['tipo_sociedade']==tipo_sociedade_name].sort_values(by=['default'])['default'], 
                    colors_values=['#FFF4BD', '#85D2D0'],
                    labels_dict={'x': 'Valor Total Pedidos', 'y': 'Quantidade', 'color': 'Default'},
                    range_x=[0, 20000],
                    nbins=2000)
    return fig

@app.callback(
    Output(sociedade_multi_dict[1]['graph_name'], 'figure'),
    Input(sociedade_multi_dict[1]['dropdown_name'], 'value'))
def update_graph(tipo_sociedade_name):
    fig = PlotHist(
                    x=df[df['tipo_sociedade']==tipo_sociedade_name].sort_values(by=['default'])['default_3months'], 
                    color=df[df['tipo_sociedade']==tipo_sociedade_name].sort_values(by=['default'])['default'],
                    colors_values=['#FFF4BD', '#85D2D0'],
                    labels_dict = {'x': 'Default Total', 'y': 'Quantidade', 'color': 'Default'},
                    range_x = [0, 3],
                    nbins=None)
    return fig

@app.callback(
    Output(year_dict['graph_name'], 'figure'),
    Input(year_dict['dropdown_name'], 'value'))
def update_graph(year):
    fig = PlotHist(
                    x=df[df['year']==year].sort_values(by=['default'])['valor_total_pedido'], 
                    color=df[df['year']==year].sort_values(by=['default'])['default'],
                    colors_values=['#FFF4BD', '#85D2D0'],
                    labels_dict = {'x': 'Valor Total Pedidos', 'y': 'Quantidade', 'color': 'Default'},
                    range_x = [0, 30000],
                    nbins=None)
    return fig

@app.callback(
    Output('default_probability', 'figure'),
    Input('opcao_tributaria', 'value'),
    Input('tipo_sociedade', 'value'),
    Input('default_3months', 'value'),
    Input('valor_vencido', 'value'),
    Input('valor_por_vencer', 'value'),
    Input('valor_quitado', 'value'),
    Input('ioi_36months', 'value'),
    Input('valor_total_pedido', 'value'),
    Input('ioi_3months', 'value'),
    Input('valor_protestos', 'value'),
    Input('quant_protestos', 'value')
    )
def ml_callback(
    opcao_tributaria, 
    tipo_sociedade, 
    default_3months, 
    valor_vencido,
    valor_por_vencer,
    valor_quitado,
    ioi_36months,
    valor_total_pedido,
    ioi_3months,
    valor_protestos,
    quant_protestos):

    coop = 1 if tipo_sociedade == 'tipo_sociedade_cooperativa' else 0
    emp_ind = 1 if tipo_sociedade == 'tipo_sociedade_empresa individual respons limitada empresaria' else 0
    lucro = 1 if opcao_tributaria == 'opcao_tributaria_lucro real' else 0
    simples = 1 if opcao_tributaria == 'opcao_tributaria_simples nacional' else 0

    
    dict_ml = {
        'default_3months': [default_3months], 
        'valor_vencido': [valor_vencido], 
        'valor_por_vencer': [valor_por_vencer], 
        'opcao_tributaria_simples nacional': [simples], 
        'valor_quitado': [valor_quitado], 
        'ioi_36months': [ioi_36months], 
        'valor_total_pedido': [valor_total_pedido], 
        'ioi_3months': [ioi_3months], 
        'valor_protestos': [valor_protestos], 
        'tipo_sociedade_empresa individual respons limitada empresaria': [emp_ind], 
        'quant_protestos': [quant_protestos], 
        'opcao_tributaria_lucro real': [lucro], 
        'tipo_sociedade_cooperativa': [coop]}

    wait = True
    prob = [[0, 0]]
    for key in dict_ml:
        wait = False
        if dict_ml[key][0] is None:
            wait = True
            break
    
    prob = [[1, 0]]
    if not wait:
        _, prob = default_prediction(dict_ml)
    prob = prob[0][1]

    fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = int(prob*100),
                title = {'text': "Probabilidade de Default (%)"},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "black"},
                    'bar': {'color': "lightgrey"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "black",
                    'steps': [
                        {'range': [0, 30], 'color': 'green'},
                        {'range': [30, 70], 'color': 'yellow'},
                        {'range': [70, 100], 'color': 'red'}],
                        })
                    )       

    return fig