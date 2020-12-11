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
    html.Div([
        html.A([
            html.Img(src='assets/logo.png',height=60)
        ],href='/')
    ]),
    dcc.Tabs(id='tabs',children=[
        dcc.Tab([pg.home],label='Home', value='tab-1',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(children=[pg.search],label='Search', value='tab-2',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab([pg.trends],label='Trends', value='tab-3',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab([pg.world],label='World', value='tab-4',style=tab_style, selected_style=selected_tab_style),
        #dcc.Tab([pg.screener],label='Screener', value='tab-5',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab([pg.compare],label='Compare', value='tab-6',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab([pg.portfolio],label='Porfolio', value='tab-7',style=tab_style, selected_style=selected_tab_style),
    ]+[dcc.Tab(value='blank',style=tab_style, selected_style=tab_style)]*6, # 탭 여백
    loading_state={'is_loding':True},colors={"primary": "#2e2e2e", "background": "grey"},style={'height':'30px','padding':'6px'}),
],style={'max-width':'1300px','margin':'0 auto'})


@app.callback(Output('symbols-search', 'options'),
            [Input('symbols-search', 'value')])
def symbols_names_callback(value):
    options_list = [{'label': i,
                     'value': j} for i, j in zip(gd.etflist['Name'], gd.etflist['Symbol'])]
    return options_list

@app.callback(Output('compare 1', 'options'),
            [Input('compare 1', 'value')])
def symbols_names_callback(value):
    options_list = [{'label': i,
                     'value': j} for i, j in zip(gd.etflist['Name'], gd.etflist['Symbol'])]
    return options_list

@app.callback(Output('compare 2', 'options'),
            [Input('compare 2', 'value')])
def symbols_names_callback(value):
    options_list = [{'label': i,
                     'value': j} for i, j in zip(gd.etflist['Name'], gd.etflist['Symbol'])]
    return options_list


@app.callback(
[Output('kospi-graph', 'figure'),Output('kosdaq-graph', 'figure'),Output('snp500-graph', 'figure')],
[Input('index-period', 'value')])
def update_figure(selected_period):
    return gd.get_indice_data('KS11',selected_period),gd.get_indice_data('KQ11',selected_period),gd.get_indice_data('US500',selected_period)

@app.callback([Output('etf-name','children'),Output('etf-chart','children'),Output('etf-info-table','children')],
[Input('search-button','n_clicks'),Input('range-slider','value')],[State('symbols-search','value')])
def show_etf_chart(n_clicks, period, symbol):
    if symbol=='':
        return (None,None,None)
    name, chart, table = gd.get_etf_chart(symbol, period)
    if n_clicks>0:
        return name, chart, table
    else:
        return (None,None,None)

@app.callback([Output('portfolio-table','children'),Output('portfolio-piechart','children')],
Input('search-button','n_clicks'),[State('symbols-search','value')])
def show_etf_chart(n_clicks, symbol):
    if symbol=='':
        return (None,None)
    table, chart = gd.get_etf_pie_chart(symbol)
    if n_clicks>0:
        return table, chart
    else:
        return (None,None)

@app.callback(Output('compare-chart','children'),
[Input('compare-button','n_clicks'),Input('compare-period','value')],[State('compare 1','value'),State('compare 2','value')])
def show_compare_chart(n_clicks, period, symbol1, symbol2):
    if symbol1=='' or symbol1=='':
        return None
    chart = gd.get_compare_chart(period, symbol1, symbol2)
    if n_clicks>0:
        return chart
    else:
        return None

@app.callback([Output('compare-table1','children'),Output('compare-table2','children')],
Input('compare-button','n_clicks'),[State('compare 1','value'),State('compare 2','value')])
def show_compare_table(n_clicks, symbol1, symbol2):
    if symbol1=='' or symbol1=='':
        return (None,None)
    table1, table2 = gd.get_compare_table(symbol1), gd.get_compare_table(symbol2)
    if n_clicks>0:
        return table1, table2
    else:
        return (None,None)

if __name__ == "__main__":
    app.run_server(debug=True)

