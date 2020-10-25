
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

import pymysql
from sqlalchemy import create_engine


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

connection = pymysql.connect(
    host='localhost',
    user='lovedh',
    password='123',
    db='etfkor',
    charset='utf8')

cursor = connection.cursor()
sql = "select * from etfList"
cursor.execute(sql)

df = pd.DataFrame(cursor.fetchall(), columns=['Symbol','Name','now_price','ex_price','market_cap','listed_shares','commission','base_index','type','listed_day'])
connection.close()

df['yield'] = (df['now_price'] - df['ex_price']) / df['ex_price'] *100

fig = px.scatter(df, x="Symbol", y="yield",
                 size="market_cap", color="type", hover_name="Name",
                 log_x=False, size_max=60)

app.layout = html.Div([
    dcc.Graph(
        id='시가총액과 수익률변화',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)