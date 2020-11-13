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
sql = """SELECT * FROM etfList WHERE Symbol IN 
(069500,360200,192090,245710,261920,195920,200250,256440,265690,291130)"""
cursor.execute(sql)

df = pd.DataFrame(cursor.fetchall(), columns=['Symbol','Name','now_price','ex_price','yield_from_ex','market_cap','listed_shares','commission','base_index','type','listed_day'])
country_code = ['KOR','CHN','VNM','USA','IND','JPN','IDN','RUS','MEX','PHL']
country = ['Korea','China','Vietnam','United States of America','India','Japan','Indonesia',
'Russia','Mexico','Philippines']
df['CODE'] = country_code
df['COUNTRY'] = country

fig = go.Figure(data=go.Choropleth(
    locations = df['CODE'],
    z = df['yield_from_ex'],
    text = df['COUNTRY'],
    colorscale = 'RdBu',
    autocolorscale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '%',
    colorbar_title = 'Yield rate%',
))
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
print(df['market_cap'], df['yield_from_ex'])
df['pn'] = ['up' if i > 0 else 'down' for i in df['yield_from_ex'] ]
df['yield_from_ex'] = abs(df['yield_from_ex'])
fig2 = px.scatter_geo(df, locations="CODE", color="pn",
                     hover_name="COUNTRY", size=df['yield_from_ex'],size_max=50,
                     projection="robinson")

fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
app = dash.Dash()
app.layout = html.Div([
    html.Div([dcc.Graph(figure=fig)]),
    html.Div([dcc.Graph(figure=fig2)])
])

app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter