from dash import dcc, html

def gen_number_input(title, id_name):
    sequence = [
        html.Div(children=[
            html.Div(children=title),
            html.Br(),
            dcc.Input(id=id_name, type='number', placeholder=title)
        ], 
        className='divBorderInput', style={'width': '45%', 'display': 'inline-block'})
        
    ]
    return sequence

ml_layout = [

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Div(children='Opção Tributária'),
                html.Br(),
                dcc.RadioItems(
                id = 'opcao_tributaria',
                options=[
                    {'label': 'Simples Nacional', 'value': 'opcao_tributaria_simples nacional'},
                    {'label': 'Lucro Real', 'value': 'opcao_tributaria_lucro real'},
                    {'label': 'Outro', 'value': 'outro'},
                ], 
                value='outro'),
            ], 
            className='divBorderInput', style={'width': '45%', 'display': 'inline-block'}),
            
            html.Div(children=[
                html.Div(children='Tipo Sociedade'),
                html.Br(),
                dcc.RadioItems(
                id='tipo_sociedade',
                options=[
                    {'label': 'Empr. Indiv. Respons. Limitada', 'value': 'tipo_sociedade_empresa individual respons limitada empresaria'},
                    {'label': 'Cooperativa', 'value': 'tipo_sociedade_cooperativa'},
                    {'label': 'Outro', 'value': 'outro'},
                ], 
                value='outro'),
            ], 
            className='divBorderInput', style={'width': '45%', 'display': 'inline-block'}),

            *gen_number_input(id_name='valor_total_pedido', title='Valor Total do Pedido'),
            *gen_number_input(id_name='valor_quitado', title='Valor Quitado'),
            *gen_number_input(id_name='valor_por_vencer', title='Valor por vencer'),
            *gen_number_input(id_name='valor_vencido', title='Valor Vencido'),
            *gen_number_input(id_name='valor_protestos', title='Valor de Protestos'),
            *gen_number_input(id_name='quant_protestos', title='Quantidade de Protestos'),
            *gen_number_input(id_name='ioi_36months', title='Intervalo Médio entre pedidos nos últimos 36 Meses (dias)'),
            *gen_number_input(id_name='ioi_3months', title='Intervalo Médio entre pedidos nos últimos 3 Meses (dias)'),
            *gen_number_input(id_name='default_3months', title='Quantidade de default nos últimos 3 Meses'),
    ], className='divBorder', style={'width': '65%', 'display': 'inline-block'}),

    html.Div(children=[                    
        dcc.Graph(id='default_probability'),
    ], 
    className='divBorderInput', style={'width': '25%', 'display': 'inline-block'}),


    ], className='divBorder')
    
]