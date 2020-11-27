#import packages
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

import lib.getfromDB as gd

#external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__)
#, external_stylesheets=external_stylesheets)

index_period = 30
tab_style = {'color': 'white','padding':'6px'}
selected_tab_style = {'padding':'6px','color': 'white','backgroundColor': '#2e2e2e'}

home = [
        dcc.RadioItems(
            id='index-period',
            options=[
                {'label': '1주일', 'value': 7},
                {'label': '1달', 'value': 30},
                {'label': '1년', 'value': 365},
                {'label': '5년', 'value': 1825}
            ],
            value=30,
            labelStyle={'display': 'inline-block'},style={'padding':'10px'}
        ),
        html.Table([
            html.Tr([
                html.Td(style={'width':'5%'}),
                html.Td([html.H5('코스피')],style={'width':'30%','textAlign':'center'}),
                html.Td([html.H5('코스닥')],style={'width':'30%','textAlign':'center'}),
                html.Td([html.H5('S&P500')],style={'width':'30%','textAlign':'center'}),
                html.Td(style={'width':'5%'})
            ]),
            html.Td(style={'width':'5%'}),
            html.Td([
                dcc.Graph(
                    id='kospi-graph',
                    figure=gd.get_indice_data('KS11')
                )
            ],style={'width':'30%'}),
            html.Td([
                dcc.Graph(
                    id='kosdaq-graph',
                    figure=gd.get_indice_data('KQ11')
                )
            ],style={'width':'30%'}),            
            html.Td([
                dcc.Graph(
                    id='snp500-graph',
                    figure=gd.get_indice_data('US500')
                )
            ],style={'width':'30%'}),
            html.Td(style={'width':'5%'})
        ],style={'width':'100%'})
    ]

app.layout = html.Div([
    html.Table([
            html.Tr(
                html.A([
                    html.Img(src='assets/logo.png',height=60)
                ],href='/')
            ),
            html.Tr(
                dcc.Dropdown(id='symbols-search',
                    multi=False,
                    placeholder="ETF 종목명을 입력하세요.",
                    style={'height': '30px','min_width':'200px','fontSize': 15,'textAlign': 'left'})
            )
    ],style={'width':'50%'}),
    dcc.Tabs(id='tabs',children=[
        dcc.Tab(label='Home', value='tab-1',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Maps', value='tab-2',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='ETFs', value='tab-3',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Compare', value='tab-4',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Porfolio', value='tab-5',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(value='blank',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(value='blank',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(value='blank',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(value='blank',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(value='blank',style=tab_style, selected_style=selected_tab_style),
    ], colors={"primary": "#2e2e2e", "background": "grey"},style={'height':'30px','padding':'6px'}),
    html.Div(home,id='tabs-content-props')
],style={'max-width':'1400px','margin':'0 auto'})


@app.callback(Output('symbols-search', 'options'),
            [Input('symbols-search', 'value')])
def symbols_names_callback(value):
    options_list = [{'label': i,
                     'value': j} for i, j in zip(gd.etflist['Name'], gd.etflist['Symbol'])]
    return options_list

@app.callback(Output('tabs-content-props', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return home
    elif tab == 'tab-2':
        return gd.get_map_data()

    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 3')
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 4')
        ])
    elif tab == 'tab-5':
        return html.Div([
            html.H3('Tab content 4')
        ])
    else:
        return None

@app.callback(
[Output('kospi-graph', 'figure'),Output('kosdaq-graph', 'figure'),Output('snp500-graph', 'figure')],
[Input('index-period', 'value')])
def update_figure(selected_period):
    return gd.get_indice_data('KS11',selected_period),gd.get_indice_data('KQ11',selected_period),gd.get_indice_data('US500',selected_period)

if __name__ == "__main__":
    app.run_server(debug=True)