import pymysql
from sqlalchemy import create_engine
import json
import pandas as pd
from datetime import datetime

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

year = datetime.today().strftime('%Y')

with open('config.json', 'r') as f:
    config = json.load(f)

HOSTNAME = config["MYSQL_INFO"]['HOSTNAME']
PORT     = config["MYSQL_INFO"]['PORT']
USERNAME = config["MYSQL_INFO"]['USERNAME']
PASSWORD = config["MYSQL_INFO"]['PASSWORD']
DATABASE = config["MYSQL_INFO"]['DATABASE']
CHARSET1 = config["MYSQL_INFO"]['CHARSET1']    # MySQL에서 사용할 캐릭터셋 이름
CHARSET2 = config["MYSQL_INFO"]['CHARSET2']    # Python에서 사용할 캐릭터셋 이름

indices = {'KS11':'코스피','KQ11':'코스닥','US500':'S&P500'}

def get_data_from_db(sql):
    connection = pymysql.connect(
        host=HOSTNAME,
        user=USERNAME,
        password=PASSWORD,
        db=DATABASE,
        charset=CHARSET1)
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()

    return data

sql = "select Symbol,Name from etfkor.etfList"
etflist = pd.DataFrame(get_data_from_db(sql), columns=['Symbol','Name'])

# HOME 지수 그래프 호출
def get_indice_data(name,index_period=30):

    if index_period == 'ytd': # ytd일 경우
        sql = "select Date, Close, Open, High, Low from etfkor."+name+" WHERE YEAR(Date)='"+year+"';"
        df = pd.DataFrame(get_data_from_db(sql), columns=['Date', 'Close', 'Open', 'High', 'Low'])
    else:
        sql = "select Date, Close, Open, High, Low from etfkor."+name
        try:
            index_period = -index_period
        except:
            index_period = -30
        df = pd.DataFrame(get_data_from_db(sql)[index_period:], columns=['Date', 'Close', 'Open', 'High', 'Low'])
    
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],increasing_line_color= 'Red', decreasing_line_color= 'Blue')],
                layout={'height':200,'width':370,'margin':{"r":0,"t":0,"l":0,"b":0}})
    fig.update_layout(xaxis=dict(visible=False,type='category',rangeslider=dict(visible=False)))
    fig.update_traces(line={'width':1}, selector=dict(type='candlestick'))
    
    return fig

# Trends ETF 트리맵 호출
def get_tree_map():

    sql = "select Name, yield_from_ex, market_cap, type1, type2 from etfkor.etfList"
    df = pd.DataFrame(get_data_from_db(sql), columns=['종목명','등락률','시가총액','유형1','유형2'])
    fig = px.treemap(df, path=['유형1','유형2','종목명'], values='시가총액',
                    color='등락률', hover_data=['종목명'],
                    color_continuous_scale='RdBu_r',
                    color_continuous_midpoint=0)
    fig.update_layout({'margin':{"r":0,"t":20,"l":0,"b":0},'height':600})
    fig.update_traces(textfont={'family':'sans-serif','size':15},textposition='middle center', selector=dict(type='treemap'))

    return fig

# WORLD 지수 트렌드 호출
def get_world_map():
    
    sql = """SELECT * FROM etfkor.indices WHERE Symbol in ('^GSPC','^FTSE','^GDAXI','^FCHI','IMOEX.ME','^N225','^HSI','000001.SS','^STI','^AXJO','^BSESN','^JKSE','^KLSE','^NZ50','^KS11','^GSPTSE','^BVSP',
    '^MXX','^IPSA','^MERV','^TA125.TA','^CASE30')"""

    df = pd.DataFrame(get_data_from_db(sql), columns=['코드','지수명','국가','국가코드','현재가','전일대비','등락률'])

    df['등락률'] = df['등락률'].str[:-1].astype(float)
    df['pn'] = ['상승' if i > 0 else '하락' for i in df['등락률']]
    df['등락률'] = abs(df['등락률'])

    fig = px.scatter_geo(df, locations="국가코드", color="pn",
                        hover_name="국가", size=df['등락률'],size_max=60,
                        hover_data=['지수명','현재가','전일대비'],
                        color_discrete_sequence=['red','blue'],
                        projection="robinson")
    fig.update_layout({'margin':{"r":10,"t":0,"l":0,"b":10},'height':600})

    return fig

def get_world_table():

    sql = "SELECT * FROM etfkor.indices"
    df = pd.DataFrame(get_data_from_db(sql), columns=['코드','지수명','국가','국가코드','현재가','전일대비','등락률'])

    df['현재가'] = df['현재가'].apply(lambda x : "{:,}".format(int(x)))
    df.rename(columns={'현재가':'현재가(달러)','등락률':'등락률(%)'}, inplace=True)

    custom_cell_conditional = [     
                        {'if': {'column_id': '코드'},'textAlign': 'left','width': '80px'},
                        {'if': {'column_id': '지수명'},'textAlign': 'left','width': '140px'},
                        {'if': {'column_id': '국가'},'textAlign': 'left','width': '80px'},
                        {'if': {'column_id': '국가코드'},'textAlign': 'left','width': '50px'},
                        {'if': {'column_id': '현재가(달러)'},'width': '70px'},
                        {'if': {'column_id': '전일대비'},'width': '70px'},
                        {'if': {'column_id': '등락률(%)'},'width': '70px'}
                    ]
    custom_data_conditional=[
                        {
                            'if': {
                            'filter_query': '{등락률(%)} contains +',
                            'column_id': '등락률(%)'
                            },
                            'color': 'Red'
                        },
                        {
                            'if': {
                            'filter_query': '{등락률(%)} contains -',
                            'column_id': '등락률(%)'
                            },
                            'color': 'Blue'
                        },
                        {
                            'if': {
                            'filter_query': '{전일대비} contains +',
                            'column_id': '전일대비'
                            },
                            'color': 'Red'
                        },
                        {
                            'if': {
                            'filter_query': '{전일대비} contains -',
                            'column_id': '전일대비'
                            },
                            'color': 'Blue'
                        },
                    ]
    
    table_left = dash_table.DataTable(
                    data=df[:int(len(df)/2)].to_dict('records'),
                    columns=[{'id': c, 'name': c} for c in df.columns],
                    style_as_list_view=True,
                    style_cell={'fontFamily': 'sans-serif', 'fontSize': '11px','padding':0},
                    style_data={'border':'0px'},
                    style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                    },
                    style_cell_conditional=custom_cell_conditional,
                    style_data_conditional=custom_data_conditional
                )

    table_right =  dash_table.DataTable(
                    data=df[int(len(df)/2):].to_dict('records'),
                    columns=[{'id': c, 'name': c} for c in df.columns],
                    style_as_list_view=True,
                    style_cell={'fontFamily': 'sans-serif', 'fontSize': '11px','padding':0},
                    style_data={'border':'0px'},
                    style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                    },
                    style_cell_conditional=custom_cell_conditional,
                    style_data_conditional=custom_data_conditional
                )  

    return table_left, table_right

# HOME 데이터 테이블 호출
def get_etf_table_by_market_cap(by):

    sql = "select Name, now_price, yield_from_ex, market_cap from etfkor.etfList"
    df = pd.DataFrame(get_data_from_db(sql), columns=['종목명','현재가','등락률','시가총액'])

    if by == '시가총액 TOP 10':
        df.sort_values(by='시가총액', ascending=False, inplace=True)
        df = df.head(20)
    elif by == '등락률 TOP 10':
        df.sort_values(by='등락률', ascending=False, inplace=True)
        df = df.head(10)
    elif by == '등락률 BOTTOM 10':
        df.sort_values(by='등락률', ascending=True, inplace=True)
        df = df.head(10)

    # 데이터 정리
    df['현재가'] = df['현재가'].apply(lambda x : "{:,}".format(int(x)))
    df['등락률'] = df['등락률'].apply(lambda x : "+"+str(x) if x>0 else str(x))
    df['시가총액'] = df['시가총액'].apply(lambda x : "{:,}".format(int(x/100000000)))
    df.rename(columns={'종목명':by,'현재가':'현재가(원)','등락률':'등락률(%)','시가총액':'시가총액(억원)'}, inplace=True)

    result = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        style_as_list_view=True,
        style_cell={'fontFamily': 'sans-serif', 'fontSize': '11px','padding':0},
        style_data={'border':'0px'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_cell_conditional=[            
            {'if': {'column_id': by},'textAlign': 'left','width': '200px'},
            {'if': {'column_id': '시가총액'},'width': '100px'},
            {'if': {'column_id': '등락률'},'width': '100px'}
        ],
        style_data_conditional=[
            {
                'if': {
                'filter_query': '{등락률(%)} contains +',
                'column_id': '등락률(%)'
                },
                'color': 'Red'
            },
            {
                'if': {
                'filter_query': '{등락률(%)} contains -',
                'column_id': '등락률(%)'
                },
                'color': 'Blue'
            },
        ]
    )

    return result

# HOME 미니맵 호출
def get_mini_treemap():

    sql = "select Name, yield_from_ex, market_cap, type1, type2 from etfkor.etfList"
    df = pd.DataFrame(get_data_from_db(sql), columns=['종목명','등락률','시가총액','유형1','유형2'])

    fig = px.treemap(df, path=['유형1','유형2','종목명'], values='시가총액',
                    color='등락률', hover_data=['종목명'],
                    color_continuous_scale='RdBu_r',
                    color_continuous_midpoint=0)
    fig.update_layout({'margin':{"r":0,"t":10,"l":0,"b":10},'width':400,'height':300})
    fig.update(layout_coloraxis_showscale=False)
    fig.update_traces(textposition='middle center', selector=dict(type='treemap'))
    result = dcc.Graph(
            id='ETF유형별 등락률',
            figure=fig
        )
    return result

# HOME pie차트 호출
def get_etf_pie_chart():
    sql = "select Name, market_cap from etfkor.etfList"

    df = pd.DataFrame(get_data_from_db(sql), columns=['종목명','시가총액'])
    df = df.head(50)
    fig = px.pie(df, values='시가총액', names='종목명')
    fig.update_layout({'title':'시장 비율','margin':{"r":0,"t":50,"l":0,"b":10},'width':350,'height':350})
    fig.update_traces(hole=.4,textposition='inside', textinfo='percent+label',showlegend=False)
    result = dcc.Graph(
            id='ETF 시장 비율',
            figure=fig
    )
    
    return result


def get_etf_single_chart(code):
    sql = "select * from etfkor."+code
    df = pd.DataFrame(get_data_from_db(sql), columns=['Date', 'Close', 'Open', 'High', 'Low', 'Volume', 'Change'])
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],increasing_line_color= 'Red', decreasing_line_color= 'Blue')],
                layout={'height':200,'width':370,'margin':{"r":0,"t":0,"l":0,"b":0}})
    fig.update_layout(xaxis=dict(visible=False,type='category',rangeslider=dict(visible=False)))
    fig.update_traces(line={'width':1}, selector=dict(type='candlestick'))
    result = dcc.Graph(figure=fig)

    return result

def get_stock_chart(symbol):

    sql = "select * from etfkor."+symbol
    df = pd.DataFrame(get_data_from_db(sql),columns=['날짜','NAV','시가','고가','저가','종가','거래량','거래대금','기초지수'])
    sql = "select * from etfkor.etfList WHERE Symbol = "+symbol
    info = pd.DataFrame(get_data_from_db(sql),columns=['코드','종목명','현재가','종가','등락률','시가총액','상장주식수','수수료','기초지수','유형1','유형2','상장일'])
    fig = go.Figure(data=[go.Scatter(x=df['날짜'],
                y=df['종가'])],
                layout={'height':200,'width':370,'margin':{"r":0,"t":0,"l":0,"b":0}})
    result = html.Div([
        html.H1(info['종목명'][0]),
        html.Table([
            html.Td([
                dcc.Graph(
                    figure = fig
                )
            ]),
            html.Td([
                
            ])
        ])


    ])

    return result