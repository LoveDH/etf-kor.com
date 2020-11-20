import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__)
#, external_stylesheets=external_stylesheets)

tab_style = {'color': 'white','padding':'6px'}
selected_tab_style = {'padding':'6px','color': 'white','backgroundColor': '#2e2e2e'}

app.layout = html.Div([
    html.Table([
            html.Td([
                html.Table([
                    html.Tr(
                        html.A([
                            html.Img(src='assets/logo.png',height=55)
                        ],style={'height':'30','valign':'middle'},href='/')
                    ),
                    html.Tr(
                         dcc.Dropdown(id='symbols-search',
                             multi=False,
                             placeholder="ETF 종목명을 입력하세요.",
                             style={'height': '30px','min_width':'200px','fontSize': 15,'textAlign': 'left'})
                    )
                ],style={'width':'80%','border':'0'})
            ])
    ],style={'width':'50%'}),
    dcc.Tabs([
        dcc.Tab(label='Home', value='tab-1',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Maps', value='tab-2',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='ETFs', value='tab-3',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Compare', value='tab-4',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(label='Porfolio', value='tab-5',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(value='blank',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(value='blank',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(value='blank',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(value='blank',style=tab_style, selected_style=selected_tab_style),
        dcc.Tab(value='blank',style=tab_style, selected_style=selected_tab_style),
    ], colors={
        "primary": "#2e2e2e",
        "background": "grey"
    },style={'height':'30px','padding':'6px'}),
    html.Div(id='tabs-content-props')
],style={'max-width':'1400px','margin':'0 auto'})


if __name__ == "__main__":
    app.run_server(debug=True)