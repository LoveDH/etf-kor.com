import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

from lib import layouts as lo
from app import app
import callbacks

tab_style = {'color': 'white','padding':'6px'}
selected_tab_style = {'padding':'6px','color': 'white','backgroundColor': '#2e2e2e'}

app.layout = html.Div([
    html.Div([
        html.A([
            html.Img(src='assets/logo.png',height=60)
        ],href='/')
    ]),
    dcc.Tabs(id='tabs',children=[
        dcc.Tab([lo.home],label='Home', value='tab-1',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(children=[lo.search],label='Search', value='tab-2',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab([lo.trends],label='Trends', value='tab-3',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab([lo.world],label='World', value='tab-4',style=tab_style, selected_style=selected_tab_style),
        #dcc.Tab([lo.screener],label='Screener', value='tab-5',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab([lo.compare],label='Compare', value='tab-6',style=tab_style, selected_style=selected_tab_style),
        #dcc.Tab([lo.portfolio],label='Porfolio', value='tab-7',style=tab_style, selected_style=selected_tab_style),
    ]+[dcc.Tab(value='blank',style=tab_style, selected_style=tab_style)]*6, # 탭 여백
    loading_state={'is_loding':True},colors={"primary": "#2e2e2e", "background": "grey"},style={'height':'30px','padding':'6px'}),
],style={'max-width':'1300px','margin':'0 auto'})

if __name__ == "__main__":
    app.run_server(debug=True)