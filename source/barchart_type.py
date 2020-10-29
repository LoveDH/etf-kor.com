
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
    user='root',
    password='rla369',
    db='etfkor',
    charset='utf8')

cursor = connection.cursor()
sql = "select * from etfList"
cursor.execute(sql)

df = pd.DataFrame(cursor.fetchall(), columns=['Symbol','Name','now_price','ex_price','yield_from_ex','market_cap','listed_shares','commission','base_index','type','listed_day'])
connection.close()

df.sort_values(['type','yield_from_ex'],ascending=[True,False], inplace=True,)

fig = px.bar(df,x='Name',y="yield_from_ex",
             color="type", hover_name="Name")

app.layout = html.Div([
    dcc.Graph(
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)