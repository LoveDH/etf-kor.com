#import packages
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

from lib import getfromDB as gd
from lib import pages as pg


app = dash.Dash(__name__)

tab_style = {'color': 'white','padding':'6px'}
selected_tab_style = {'padding':'6px','color': 'white','backgroundColor': '#2e2e2e'}

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
        dcc.Tab([pg.home],label='Home', value='tab-1',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab([pg.trends],label='Trends', value='tab-2',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab([pg.world],label='World', value='tab-3',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab([pg.etfs],label='ETFs', value='tab-4',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Compare', value='tab-5',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Porfolio', value='tab-6',style=tab_style, selected_style=selected_tab_style),
    ]+[dcc.Tab(value='blank',style=tab_style, selected_style=selected_tab_style)]*6, # 탭 여백
    colors={"primary": "#2e2e2e", "background": "grey"},style={'height':'30px','padding':'6px'}),
    html.Div(id='tabs-content-props',style={'width':'100%'})
],style={'max-width':'1300px','margin':'0 auto'})


@app.callback(Output('symbols-search', 'options'),
            [Input('symbols-search', 'value')])
def symbols_names_callback(value):
    options_list = [{'label': i,
                     'value': j} for i, j in zip(gd.etflist['Name'], gd.etflist['Symbol'])]
    return options_list

@app.callback(
[Output('kospi-graph', 'figure'),Output('kosdaq-graph', 'figure'),Output('snp500-graph', 'figure')],
[Input('index-period', 'value')])
def update_figure(selected_period):
    return gd.get_indice_data('KS11',selected_period),gd.get_indice_data('KQ11',selected_period),gd.get_indice_data('US500',selected_period)

if __name__ == "__main__":
    app.run_server(debug=True)


# @app.callback(Output('tabs-content-props', 'children'),
#               [Input('tabs', 'value')])
# def render_content(tab):
#     if tab == 'tab-1':
#         return pg.home
#     elif tab == 'tab-2':
#         return  pg.trends
#     elif tab == 'tab-3':
#         return html.Div([
#             gd.get_world_map()
#         ])
#     elif tab == 'tab-4':
#         return html.Div([
#             dcc.RadioItems(
#                 id='stock-period',
#                 options=[
#                     {'label': '1주일', 'value': 7},
#                     {'label': '1개월', 'value': 30},
#                     {'label': '3개월', 'value': 90},
#                     {'label': '6개월', 'value': 180},
#                     {'label': '1년', 'value': 365},
#                     {'label': 'YTD', 'value': 'ytd'},
#                     {'label': '5년', 'value': 1825}
#                 ],
#                 value=30,
#                 labelStyle={'display': 'inline-block'},style={'padding':'10px'}
#             ),
#             html.Div([gd.get_stock_chart('069500')],id='stock-chart')
#         ])
#     elif tab == 'tab-5':
#         return html.Div([
#             html.H3('Tab content 4')
#         ])
#     elif tab == 'tab-6':
#         return html.Div([
#             html.H3('Tab content 4')
#         ])
#     else:
#         return None