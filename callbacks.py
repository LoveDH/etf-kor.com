from dash.dependencies import Input, Output, State
from lib import getfromDB as gd
from app import app

options_list = [{'label': i,'value': j} for i, j in zip(gd.etflist['Name'], gd.etflist['Symbol'])]
@app.callback([Output('symbols-search', 'options'),Output('compare 1', 'options'),Output('compare 2', 'options')],
            Input('symbols-search','value'))
def symbols_names_callback(value):
    return options_list, options_list, options_list

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

@app.callback(Output('etf-history','children'),
Input('search-button','n_clicks'),[State('symbols-search','value')])
def show_etf_chart(n_clicks, symbol):
    if symbol=='':
        return None
    table = gd.get_history_table(symbol)
    if n_clicks>0:
        return table
    else:
        return None

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

@app.callback(Output('compare-table','children'),
Input('compare-button','n_clicks'),[State('compare 1','value'),State('compare 2','value')])
def show_compare_table(n_clicks, symbol1, symbol2):
    if symbol1=='' or symbol2=='':
        return None
    compare_table = gd.get_compare_table(symbol1,symbol2)
    if n_clicks>0:
        return compare_table
    else:
        return None