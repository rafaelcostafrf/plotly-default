from dash import dcc, html

def SingleGraph(title, figure):
    segment = [
        html.Br(),
        
        html.Div(
            children=[
                    html.H2(
                    children=title),

                    dcc.Graph(
                        figure=figure,
                    ),
                    ],
            style={'padding': '30px'},
            className='divBorder')
            ]
    return segment


def gen_dict(title, graph_name, dropdown_name, dropdown_options):
    dictionary = {
        'title': title, 
        'graph_name': graph_name, 
        'dropdown_name': dropdown_name, 
        'dropdown_options': dropdown_options}
    return dictionary


def MultiGraphDropDown(title, list_of_dict):
    higher_segment = []
    for item in list_of_dict:
        segment_piece = [
            html.Div(
            children=[
                    html.H4(children=item['title']),

                    dcc.Dropdown(
                        id=item['dropdown_name'],
                        options=item['dropdown_options'],
                        value=item['dropdown_options'][0]['value'],
                        style={
                            'width': '70%',
                            'align-items': 'left', 
                            'justify-content': 'left',
                            'margin-left':'2px',
                        }
                    ),

                    dcc.Graph(
                        id=item['graph_name'],
                    )
            ], 
            style={'width': '45%', 'display': 'inline-block', 'margin-left': '10px'}, 
            className='divBorderHigher'),
        ]
        higher_segment += segment_piece
    

    segment = [
        html.Br(),

        html.Div(
            children=[
                html.H3(children=title),
                *higher_segment,
            ], className='divBorder')
        ]
    return segment

def SingleDropdown(dict):
    segment = [
        html.Br(), 

        html.Div(
        children=[
                html.H4(children=dict['title']),

                dcc.Dropdown(
                    id=dict['dropdown_name'],
                    options=dict['dropdown_options'],
                    value=dict['dropdown_options'][0]['value'],
                    style={
                        'width': '70%',
                        'align-items': 'left', 
                        'justify-content': 'left',
                        'margin-left':'2px',
                    }
                ),

                dcc.Graph(
                    id=dict['graph_name'],
                )
        ], 
        style={}, 
        className='divBorder'),
    ]
    return segment