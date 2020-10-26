import plotly.graph_objects as go

import pandas as pd
from datetime import datetime
import pymysql.cursors

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='rla369',
    db='etfkor',
    charset='utf8')

cursor = connection.cursor()
sql = "select * from etfkor.069500"
cursor.execute(sql)

df = pd.DataFrame(cursor.fetchall(), columns = ['날짜','NAV','시가','고가','저가','종가','거래량','거래대금','기초지수'])
connection.close()

fig = go.Figure(data=[go.Candlestick(x=df['날짜'],
                open=df['시가'],
                high=df['고가'],
                low=df['저가'],
                close=df['종가'])])

fig.show()