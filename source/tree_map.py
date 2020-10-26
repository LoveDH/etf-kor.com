
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np

import pymysql
from sqlalchemy import create_engine


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
connection.close()


fig = px.treemap(df, path=['type','Name'], values='market_cap',
                  color='yield_from_ex', hover_data=['Name'],
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=0)

app.layout = html.Div([
    dcc.Graph(
        id='ETF유형별 등락률',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)