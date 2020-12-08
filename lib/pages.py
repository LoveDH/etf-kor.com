import dash_core_components as dcc
import dash_html_components as html
import lib.getfromDB as gd

# 홈 화면
home =  html.Div([
    dcc.RadioItems(
        id='index-period',
        options=[
            {'label': '1주일', 'value': 7},
            {'label': '1개월', 'value': 30},
            {'label': '3개월', 'value': 90},
            {'label': '6개월', 'value': 180},
            {'label': '1년', 'value': 365},
            {'label': 'YTD', 'value': 'ytd'},
            {'label': '5년', 'value': 1825}
        ],
        value=30,
        labelStyle={'display': 'inline-block'},style={'padding':'10px'}
    ),
    html.Table([
        html.Tr([
            html.Td(style={'width':'5%'}),
            html.Td([html.H4('코스피')],style={'width':'30%','textAlign':'center'}),
            html.Td([html.H4('코스닥')],style={'width':'30%','textAlign':'center'}),
            html.Td([html.H4('S&P500')],style={'width':'30%','textAlign':'center'}),
            html.Td(style={'width':'5%'})
        ]),
        html.Td(style={'width':'5%'}),
        html.Td([
            dcc.Graph(
                id='kospi-graph',
                figure=gd.get_indice_data('KS11')
            )
        ],style={'width':'30%'}),
        html.Td([
            dcc.Graph(
                id='kosdaq-graph',
                figure=gd.get_indice_data('KQ11')
            )
        ],style={'width':'30%'}),            
        html.Td([
            dcc.Graph(
                id='snp500-graph',
                figure=gd.get_indice_data('US500')
            )
        ],style={'width':'30%'}),
        html.Td(style={'width':'5%'})
    ],style={'width':'100%'}),
    html.Div(style={'padding':'10px'}),
    html.Table([
        html.Tr([
            html.Td([
                gd.get_etf_table_by_market_cap('시가총액 TOP 10')
            ],style={'width':'32%'}),
            html.Td(style={'width':'2%'}),
            html.Td([
                gd.get_etf_table_by_market_cap('등락률 TOP 10'),
                gd.get_etf_table_by_market_cap('등락률 BOTTOM 10'),
            ],style={'width':'32%'}),
            html.Td(style={'width':'2%'}),
            html.Td([
                html.Tr([gd.get_mini_treemap()]),
                html.Tr([gd.get_etf_pie_chart()])
            ],style={'width':'26%'}),
        ]),
        html.Tr([
            html.Td(),
            html.Td(),
            html.Td(),
        ]),
    ])
])

# 검색
search = html.Div([
    html.Table([
        html.Tr([
            html.Td([
                dcc.Dropdown(id='symbols-search',
                    multi=False,
                    placeholder="ETF 종목명을 입력하세요.",
                    value='',
                    style={'height':'30px','min_width':'100px','fontSize': 15,'textAlign': 'left'})
            ]),
            html.Td([
                html.Button('search', id='search-button', n_clicks=0)
            ])
        ])
    ],style={'width':700}),
    html.Div(id='etf-info')
])

# 트렌드
trends = html.Div([
    html.Table([
        html.Td([
            dcc.Slider(
                id='trends-slider',
                min=1,
                max=365,
                step=1,
                value=1,
                marks={
                    1:'1일',
                    30:'1개월',
                    90:'3개월',
                    180:'6개월',
                    365:'1년'
                }
            ),
        ]),
        html.Td(id='days-text')
    ],style={'width':600,'padding':'10px'}),
    dcc.Graph(
        id='etf-fluct-rate',
        figure=gd.get_tree_map()
    )
])

@app.callback(
    Output('slider-output-container', 'children'),
    [Input('my-slider', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)

# 세계 지수
world_indice_table_l, world_indice_table_r = gd.get_world_table()
world = html.Div([
    dcc.Graph(
        id='world-map',
        figure=gd.get_world_map()
    ),
    html.Div([
        html.Td([world_indice_table_l],style={'width':'49%'}),
        html.Td(style={'width':'2%'}),
        html.Td([world_indice_table_r],style={'width':'49%'})
    ])
])

# etf 종목 정보
stock_chart = html.Div([
    dcc.RadioItems(
        id='stock-period',
        options=[
            {'label': '1주일', 'value': 7},
            {'label': '1개월', 'value': 30},
            {'label': '3개월', 'value': 90},
            {'label': '6개월', 'value': 180},
            {'label': '1년', 'value': 365},
            {'label': 'YTD', 'value': 'ytd'},
            {'label': '5년', 'value': 1825}
        ],
        value=30,
        labelStyle={'display': 'inline-block'},style={'padding':'10px'}
    ),
    html.Div([gd.get_stock_chart('069500')],id='stock-chart')
])

screener = None
compare = None
portfolio = None