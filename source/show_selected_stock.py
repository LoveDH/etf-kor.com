import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

import pymysql
from sqlalchemy import create_engine

from datetime import datetime, timedelta


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='rla369',
    db='etfkor',
    charset='utf8')

cursor = connection.cursor()
sql = "select * from etfList"
cursor.execute(sql)

df = pd.DataFrame(cursor.fetchall(), columns=['Symbol','Name','now_price','ex_price','yield_from_ex','market_cap','listed_shares','commission','base_index','type','listed_day'])


# app.layout = html.Div([
#     dcc.Graph(
#         id='시가총액과 수익률변화',
#         figure=fig
#     )
# ])

symbols_list = pd.DataFrame(df, columns=['Symbol','Name'])
type_list = df['type'].unique()

# Main Div (1st level)
app.layout = html.Div([

    # Sub-Div (2nd level)
    # Dashboard Title
    # html.Div([html.H1(children='Stock Price Dashboard',
    #                   className='twelve columns',
    #                   style={'text-align': 'center',
    #                          'margin': '2% 0% 3% 0%',
    #                          'letter-spacing': 2})
    #           ], className='row'),

    # Sub-Div (2nd level)
    # DropDown
    html.Div([dcc.Dropdown(id='symbols-dropdown1',
                           multi=True,
                           placeholder="Please select a stock",
                           style={'height': '40px',
                                  'fontSize': 20,
                                  'margin': '2% 0% 7% 0%',
                                  'textAlign': 'center'})
              ], style={'align': 'center'}, className='row six columns offset-by-three'),

    # Sub-Div (2nd level)
    # Date picker and Button
    html.Div([
        # Update Button
        html.Button(id='update-button1',
                    children='Update',
                    n_clicks=0,
                    style={'fontSize': 18,
                           'fontWeight': 'normal',
                           'height': '40px',
                           'width': '150px'},
                    className='two columns button-primary')

    ], style={'margin': '2% 0% 6% 10%', 'float': 'center'}, className='row'),

    # Sub-Div (2nd level)
    # Stocks Graph
    html.Div([dcc.Graph(id='data-plot1')], className='row')
    ,

    # type
    html.Div([dcc.Dropdown(id='symbols-dropdown2',
                           multi=True,
                           placeholder="Please select a type",
                           style={'height': '40px',
                                  'fontSize': 20,
                                  'margin': '2% 0% 7% 0%',
                                  'textAlign': 'center'})
              ], style={'align': 'center'}, className='row six columns offset-by-three'),

    html.Div([
        # Update Button
        html.Button(id='update-button2',
                    children='Update',
                    n_clicks=0,
                    style={'fontSize': 18,
                           'fontWeight': 'normal',
                           'height': '40px',
                           'width': '150px'},
                    className='two columns button-primary')

        ], style={'margin': '2% 0% 6% 10%', 'float': 'center'}, className='row'),
    
    html.Div([dcc.Graph(id='data-plot2')], className='row')

], className='ten columns offset-by-one')

@app.callback(Output('symbols-dropdown1', 'options'),
            [Input('symbols-dropdown1', 'value')])
def symbols_names_callback(value):
    options_list = [{'label': symbols_list.iloc[i]['Name'],
                     'value': symbols_list.iloc[i]['Symbol']} for i in range(0, len(symbols_list))]
    return options_list

@app.callback(Output('symbols-dropdown2', 'options'),
            [Input('symbols-dropdown2', 'value')])
def symbols_names_callback(value):
    options_list = [{'label': type_list[i],
                     'value': type_list[i]} for i in range(0, len(type_list))]
    return options_list



# Custom Error Classes

class StartDateError(Exception):
    pass

class NoneValueError(Exception):
    pass

class StocksSelectedError(Exception):
    pass

@app.callback(Output('data-plot1', 'figure'),
              [Input('update-button1', 'n_clicks')],
                State('symbols-dropdown1', 'value'))
def graph_callback(n_clicks, selected_symbols):
    empty_layout = dict(data=[], layout=go.Layout(title=' closing prices',
                                                xaxis={'title': 'Date'},
                                                yaxis={'title': 'Closing Price'},
                                                font={'family': 'verdana', 'size': 15, 'color': '#606060'}))
    if n_clicks>0:
        try:
            # Error Checking on Inputs
            if selected_symbols is None:
                raise NoneValueError("ERROR : Start/End date or selected symbols is None!")
            if len(selected_symbols) == 0:
                raise StocksSelectedError("ERROR : No stocks selected!")
            
            df_list = []

            for symbol in selected_symbols:
                sql = "select * from etfkor."+symbol
                cursor.execute(sql)
                stock_df = pd.DataFrame(cursor.fetchall(),columns=['날짜','NAV','시가','고가','저가','종가','거래량','거래대금','기초지수'])
                
                df_list.append(stock_df)

            for i in range(0, len(df_list)):
                df_list[i].name = symbols_list[symbols_list['Symbol']==selected_symbols[i]].iloc[0,1]

            
            data = [go.Scatter(x=df['날짜'], y=df['종가'], mode='lines', name=df.name) for df in df_list]
            layout = go.Layout(title='종목별 종가',
                                xaxis={'title': 'Date'},
                                yaxis={'title': 'Closing Price'},
                                font={'family': 'verdana', 'size': 15, 'color': '#606060'})
            fig = dict(data=data, layout=layout)
            return fig

        # Exception Handling
        except StartDateError as e:
            print(e)
            return empty_layout
        except NoneValueError as e:
            print(e)
            return empty_layout
        except StocksSelectedError as e:
            print(e)
            return empty_layout
        except Exception as e:
            print(e)            

    else:
        return empty_layout

@app.callback(Output('data-plot2', 'figure'),
              [Input('update-button2', 'n_clicks')],
                State('symbols-dropdown2', 'value'))
def graph_callback(n_clicks, selected_types):
    empty_layout = dict(data=[], layout=go.Layout(title=' Yield from yesterday',
                                                xaxis={'title': 'Ticker'},
                                                yaxis={'title': 'Yield'},
                                                font={'family': 'verdana', 'size': 15, 'color': '#606060'}))

    if n_clicks>0:

        try:
            # Error Checking on Inputs
            if selected_types is None:
                raise NoneValueError("ERROR : Start/End date or selected symbols is None!")
            if len(selected_types) == 0:
                raise StocksSelectedError("ERROR : No stocks selected!")

            df_list = pd.DataFrame(columns=df.columns)

            for ttype in selected_types:

                stock_df = df[df['type']==ttype]
                stock_df.sort_values('yield_from_ex',axis=0,ascending=False,inplace=True)
                df_list = df_list.append(stock_df)
            
            fig = px.bar(df_list,x='Name',y="yield_from_ex",
                    color="type", hover_name="Name")

            return fig

        # Exception Handling
        except StartDateError as e:

            print(e)
            return empty_layout
        except NoneValueError as e:
            print(e)
            return empty_layout
        except StocksSelectedError as e:
            print(e)
            return empty_layout
        except Exception as e:
            print(e)            

    else:
        return empty_layout


if __name__ == '__main__':
    app.run_server(debug=True)