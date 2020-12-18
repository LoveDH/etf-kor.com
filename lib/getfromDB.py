from io import DEFAULT_BUFFER_SIZE
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

# HOME 데이터 테이블 호출
def get_etf_table_by_market_cap(by):

    sql = "select Name, now_price, yield_from_ex, market_cap from etfkor.etfList"
    df = pd.DataFrame(get_data_from_db(sql), columns=['종목명','현재가','등락률','시가총액'])

    if by == '시가총액 TOP 20':
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
    fig.update_layout({'margin':{"r":0,"t":20,"l":0,"b":10},'width':400,'height':300})
    fig.update(layout_coloraxis_showscale=False)
    fig.update_traces(textposition='middle center', selector=dict(type='treemap'))
    fig.data[0].hovertemplate='%{label}'
    result = dcc.Graph(
            id='ETF유형별 등락률',
            figure=fig,
            config={'staticPlot':True}
        )
    return result

# HOME pie차트 호출
def get_etf_pie_chart_top10():
    sql = "select Name, market_cap from etfkor.etfList"

    df = pd.DataFrame(get_data_from_db(sql), columns=['종목명','시가총액'])
    df = df.head(10)
    fig = px.pie(df, values='시가총액', names='종목명')
    fig.update_layout({'title':'시장 비율','margin':{"r":0,"t":50,"l":0,"b":10},'width':350,'height':350})
    fig.update_traces(hole=.4,textposition='inside', textinfo='percent+label',showlegend=False)
    result = dcc.Graph(
            id='ETF 시장 비율',
            figure=fig
    )
    return result

# Trends ETF 트리맵 호출
def get_tree_map():

    sql = "select Name, yield_from_ex, market_cap, type1, type2, listed_day from etfkor.etfList"
    df = pd.DataFrame(get_data_from_db(sql), columns=['종목명','등락률','시가총액','유형1','유형2','상장일'])
    fig = px.treemap(df, path=['유형1','유형2','종목명'], values='시가총액',
                    color='등락률', hover_data=['종목명','상장일'],
                    color_continuous_scale='RdBu_r',
                    color_continuous_midpoint=0)
    fig.update_layout({'margin':{"r":0,"t":15,"l":0,"b":0},'height':600})
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
                        hover_name="국가", size=df['등락률'],size_max=70,
                        hover_data=['지수명','현재가','전일대비'],
                        color_discrete_sequence=['red','blue'],
                        projection="robinson")
    fig.update_layout({'margin':{"r":10,"t":0,"l":0,"b":10},'height':600})

    return fig

# World 세계지수 데이터 테이블 호출
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



# Search etf 차트 호출
def get_etf_chart(symbol, period):
    # 차트
    if period==400:
        sql = "select * from etfkor."+symbol
        df = pd.DataFrame(get_data_from_db(sql),columns=['날짜','NAV','시가','고가','저가','종가','거래량','거래대금','기초지수'])
    else:
        sql = "select * from etfkor."+symbol
        df = pd.DataFrame(get_data_from_db(sql)[-period:],columns=['날짜','NAV','시가','고가','저가','종가','거래량','거래대금','기초지수'])
    
    # # 이동평균
    # df['5일'] = df['종가'].rolling(5).mean()
    # df['20일'] = df['종가'].rolling(20).mean()

    fig = go.Figure(data=[go.Candlestick(x=df['날짜'],
                open=df['시가'],
                high=df['고가'],
                low=df['저가'],
                close=df['종가'],increasing_line_color= 'Red', decreasing_line_color= 'Blue')],
                layout={'height':400,'width':640,'margin':{"r":0,"t":0,"l":0,"b":0}})
    fig.update_layout(yaxis=dict(tickformat="digit",autorange=True,fixedrange=False))
    fig.update_traces(line={'width':1}, selector=dict(type='candlestick'))
    chart = dcc.Graph(
        figure=fig
    )

    # 테이블
    sql = "select * from etfkor.etfList WHERE Symbol = "+symbol
    info_table = pd.DataFrame(get_data_from_db(sql),columns=['코드','종목명','현재가','전일종가','등락률','시가총액','상장주식수','수수료','기초지수','대분류','소분류','상장일'])
    name = info_table['종목명'][0]
    info_table['현재가'] = info_table['현재가'].apply(lambda x : "{:,}".format(int(x)))
    info_table['전일종가'] = info_table['전일종가'].apply(lambda x : "{:,}".format(int(x)))
    info_table['상장주식수'] = info_table['상장주식수'].apply(lambda x : "{:,}".format(int(x)))
    info_table['등락률'] = info_table['등락률'].apply(lambda x : "+"+str(x)+'%' if x>0 else str(x)+'%')
    info_table['수수료'] = info_table['수수료'].apply(lambda x : str(x)+'%' if x>0 else str(x))
    info_table['시가총액'] = info_table['시가총액'].apply(lambda x : "{:,}".format(int(x/100000000))+'(억원)')
    
    info_table = info_table.T
    info_table.rename(columns={0: "value"},inplace=True)
    info_table.reset_index(inplace=True)

    info_table = dash_table.DataTable(
        data=info_table.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in info_table.columns],
        style_as_list_view=True,
        style_cell={'fontFamily': 'sans-serif', 'fontSize': 15,'padding':0},
        style_data={'border':'0px'},
        style_header={
            'display': 'none'
        },
        style_cell_conditional=[            
            {'if': {'column_id': 'index'},'textAlign': 'left','width': '100px','fontWeight': 'bold'},
        ],
        style_data_conditional=[
            {
                'if': {
                'filter_query': '{value} contains +',
                'column_id': 'value'
                },
                'color': 'Red'
            },
            {
                'if': {
                'filter_query': '{value} contains -',
                'column_id': 'value'
                },
                'color': 'Blue'
            },
        ]
    )
    return name, chart, info_table

# Search etf 포트폴리오 구성 파이 차트 호출
def get_etf_pie_chart(symbol):
    sql = "select 종목, 계약수, 금액, 비중 from etfkor."+symbol+'_pf'

    df = pd.DataFrame(get_data_from_db(sql),columns=['종목','계약수','금액','비중'])
    fig = px.pie(df.head(10), values='비중', names='종목')
    fig.update_layout({'title':'TOP10 구성 비율','margin':{"r":0,"t":50,"l":0,"b":10},'width':350,'height':350})
    fig.update_traces(hole=.4, textinfo='percent+label',showlegend=False)
    result = dcc.Graph(
            id='포트폴리오 비율',
            figure=fig
    )

    pf_table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        style_as_list_view=True,
        page_size=10,
        style_cell={'fontFamily': 'sans-serif', 'fontSize': 11,'padding':0},
        style_data={'border':'0px'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_cell_conditional=[            
            {'if': {'column_id': '종목'},'textAlign': 'left','width': '100px','fontWeight': 'bold'},
        ]
    )
    return pf_table, result

#Search etf history 호출
def get_history_table(symbol):
    sql = "select 날짜, NAV, 시가, 고가, 저가, 종가, 거래량, 거래대금 from etfkor."+symbol
    df = pd.DataFrame(get_data_from_db(sql),columns=['날짜','NAV','시가','고가','저가','종가','거래량','거래대금'])
    df['날짜'] = df['날짜'].apply(lambda x: x.strftime('%Y-%m-%d'))
    for col in ['시가','고가','저가','종가','거래량','거래대금']:
        df[col] =df[col].apply(lambda x : "{:,}".format(int(x)))
    df.sort_values('날짜',ascending=False,inplace=True)
    history = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        style_as_list_view=True,
        page_size=10,
        style_cell={'fontFamily': 'sans-serif', 'fontSize': '11px','padding':0},
        style_data={'border':'0px'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_cell_conditional=[            
            {'if': {'column_id': '날짜'},'textAlign': 'left','width': '200px'},
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

    return history


# Compare 수익률 비교 차트
def get_compare_chart(period, symbol1,symbol2):
    name1 = list(etflist.loc[etflist['Symbol']==symbol1,'Name'])[0]
    name2 = list(etflist.loc[etflist['Symbol']==symbol2,'Name'])[0]
    
    sql1 = "select 날짜, 종가 from etfkor."+symbol1
    sql2 = "select 날짜, 종가 from etfkor."+symbol2

    if period == 'all':
        df1 = pd.DataFrame(get_data_from_db(sql1),columns=['날짜',name1])
        df2 = pd.DataFrame(get_data_from_db(sql2),columns=['날짜',name2])
    else:
        try:
            df1 = pd.DataFrame(get_data_from_db(sql1)[-period:],columns=['날짜',name1])
        except:
            df1 = pd.DataFrame(get_data_from_db(sql1),columns=['날짜',name1])

        try:
            df2 = pd.DataFrame(get_data_from_db(sql2)[-period:],columns=['날짜',name2])
        except:
            df2 = pd.DataFrame(get_data_from_db(sql2),columns=['날짜',name2])

    merged_df = pd.merge(left=df1, right=df2, how='outer', on='날짜')
    merged_df.fillna(method='bfill',inplace=True)

    # 수익률 계산
    merged_df[name1] = (merged_df[name1]/merged_df.loc[0,name1]-1)*100
    merged_df[name2] = (merged_df[name2]/merged_df.loc[0,name2]-1)*100
    merged_df.set_index('날짜',drop=True,inplace=True)

    fig = px.line(merged_df, x=merged_df.index, y=[name1,name2])
    fig.update_layout({'margin':{"r":0,"t":0,"l":0,"b":100},'yaxis_title':"수익률(%)"})
    result = dcc.Graph(
            id='수익률 비교차트',
            figure=fig
    )
    return result

# Compare 비교 테이블 생성
def get_compare_table(symbol1,symbol2):
    
    sql = "select * from etfkor.etfList WHERE Symbol IN ("+symbol1+','+symbol2+')'
    info_table = pd.DataFrame(get_data_from_db(sql),columns=['코드','종목명','현재가','전일종가','등락률','시가총액(억원)','상장주식수','수수료','기초지수','대분류','소분류','상장일'])
    for col in ['현재가','전일종가','상장주식수']:
        info_table[col] = info_table[col].apply(lambda x : "{:,}".format(int(x)))
    info_table['등락률'] = info_table['등락률'].apply(lambda x : "+"+str(x)+'%' if x>0 else str(x)+'%')
    info_table['수수료'] = info_table['수수료'].apply(lambda x : str(x)+'%' if x>0 else str(x))
    info_table['시가총액(억원)'] = info_table['시가총액(억원)'].apply(lambda x : "{:,}".format(int(x/100000000)))
    name1, name2 = info_table['종목명'][0], info_table['종목명'][1]
    info_table.set_index('종목명',drop=True,inplace=True)
    info_table = info_table.T
    info_table.reset_index(inplace=True)
    
    info_table = info_table[[name1,'index',name2]]
    info_table.rename(columns={'index':'종목명'},inplace=True)
    info_table = dash_table.DataTable(
        data=info_table.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in info_table.columns],
        style_as_list_view=True,
        style_cell={'fontFamily': 'sans-serif', 'fontSize': 15,'padding':0},
        style_data={'border':'0px'},
        style_header={
            'fontSize':15
        },
        style_cell_conditional=[            
            {'if': {'column_id': '종목명'},'textAlign': 'center','width': '30%','fontWeight': 'bold'},
            {'if': {'column_id': name1},'textAlign': 'right','width': '35%'},
            {'if': {'column_id': name2},'textAlign': 'left','width': '35%'},
        ],
    )
    return info_table