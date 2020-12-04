#import packages
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

import lib.getfromDB as gd


app = dash.Dash(__name__)

tab_style = {'color': 'white','padding':'6px'}
selected_tab_style = {'padding':'6px','color': 'white','backgroundColor': '#2e2e2e'}

home = [
        dcc.RadioItems(
            id='index-period',
            options=[
                {'label': '1주일', 'value': 7},
                {'label': '1개월', 'value': 30},
                {'label': '3개월', 'value': 90},
                {'label': '6개월', 'value': 180},
                {'label': '1년', 'value': 365},
                {'label': 'YTD', 'value': 'ytd'},
                {'label': '5년', 'value': 1825}
            ],
            value=30,
            labelStyle={'display': 'inline-block'},style={'padding':'10px'}
        ),
        html.Table([
            html.Tr([
                html.Td(style={'width':'5%'}),
                html.Td([html.H4('코스피')],style={'width':'30%','textAlign':'center'}),
                html.Td([html.H4('코스닥')],style={'width':'30%','textAlign':'center'}),
                html.Td([html.H4('S&P500')],style={'width':'30%','textAlign':'center'}),
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
        ],style={'width':'100%'}),
        html.Div(style={'padding':'10px'}),
        html.Table([
            html.Tr([
                html.Td([
                    gd.get_etf_table_by_market_cap('시가총액 TOP 10')
                ],style={'width':'32%'}),
                html.Td(style={'width':'2%'}),
                html.Td([
                    gd.get_etf_table_by_market_cap('등락률 TOP 10'),
                    gd.get_etf_table_by_market_cap('등락률 BOTTOM 10'),
                ],style={'width':'32%'}),
                html.Td(style={'width':'2%'}),
                html.Td([
                    html.Tr([gd.get_mini_treemap()]),
                    html.Tr([gd.get_etf_pie_chart()])
                ],style={'width':'26%'}),
            ]),
            html.Tr([
                html.Td(),
                html.Td(),
                html.Td(),
            ]),
        ])
    ]

app.layout = html.Div([
    html.Table([
            html.Tr(
                html.A([
                    html.Img(src='assets/logo.png',height=60)
                ],href='/')
            ),
            html.Tr([
                html.Td([
                    dcc.Dropdown(id='symbols-search',
                        multi=False,
                        placeholder="ETF 종목명을 입력하세요.",
                        value='',
                        style={'height':'30px','min_width':'100px','fontSize': 15,'textAlign': 'left'})
                ]),
                html.Td([
                    html.Button('search', id='search-button', n_clicks=0)
                ])
            ])
    ],style={'width':'40%'}),
    dcc.Tabs(id='tabs',children=[
        dcc.Tab(label='Home', value='tab-1',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Trends', value='tab-2',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='World', value='tab-3',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='ETFs', value='tab-4',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Compare', value='tab-5',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Porfolio', value='tab-6',style=tab_style, selected_style=selected_tab_style),
    ]+[dcc.Tab(value='blank',style=tab_style, selected_style=selected_tab_style)]*6, # 탭 여백
    colors={"primary": "#2e2e2e", "background": "grey"},style={'height':'30px','padding':'6px'}),
    html.Div(home,id='tabs-content-props',style={'width':'100%'})
],style={'max-width':'1300px','margin':'0 auto'})


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
        return  html.Div([
            gd.get_tree_map()
        ])
    elif tab == 'tab-3':
        return html.Div([
            gd.get_world_map()
        ])
    elif tab == 'tab-4':
        return html.Div([
            dcc.RadioItems(
                id='stock-period',
                options=[
                    {'label': '1주일', 'value': 7},
                    {'label': '1개월', 'value': 30},
                    {'label': '3개월', 'value': 90},
                    {'label': '6개월', 'value': 180},
                    {'label': '1년', 'value': 365},
                    {'label': 'YTD', 'value': 'ytd'},
                    {'label': '5년', 'value': 1825}
                ],
                value=30,
                labelStyle={'display': 'inline-block'},style={'padding':'10px'}
            ),
            html.Div([gd.get_stock_chart('069500')],id='stock-chart')
        ])
    elif tab == 'tab-5':
        return html.Div([
            html.H3('Tab content 4')
        ])
    elif tab == 'tab-6':
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

# @app.callback(
#     Output('tabs-content-props', 'children'),
#     [Input('search-button','n_clicks')],
#     State('symbols-search','value'))
# def show_stock_chart(n_click, selected_symbol):

#     if n_click > 0:
#         return 'tab-4'
#     else:
#         return 'tab-1'


if __name__ == "__main__":
    app.run_server(debug=True)