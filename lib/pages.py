import dash_core_components as dcc
import dash_html_components as html
import lib.getfromDB as gd

# 홈 화면
home =  html.Div([
    dcc.RadioItems(
        id='index-period',
        options=[
            {'label': '1주일', 'value': 7},
            {'label': '1개월', 'value': 31},
            {'label': '3개월', 'value': 92},
            {'label': '6개월', 'value': 183},
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
                gd.get_etf_table_by_market_cap('시가총액 TOP 20')
            ],style={'width':'32%'}),
            html.Td(style={'width':'2%'}),
            html.Td([
                gd.get_etf_table_by_market_cap('등락률 TOP 10'),
                gd.get_etf_table_by_market_cap('등락률 BOTTOM 10'),
            ],style={'width':'32%'}),
            html.Td(style={'width':'2%'}),
            html.Td([
                html.Tr([gd.get_mini_treemap()]),
                html.Tr([gd.get_etf_pie_chart_top10()])
            ],style={'width':'26%'}),
        ]),
    ])
],style={'textAlign': 'center'})

# 검색
search = html.Div([
    html.Div([
        html.Table([
            html.Tr([
                html.Td(style={'width':'5%'}),
                html.Td([
                    dcc.Dropdown(id='symbols-search',
                        multi=False,
                        placeholder="ETF 종목명을 입력하세요.",
                        value='',
                        style={'height':'30px','min_width':'100px','fontSize': 15,'textAlign': 'left'})
                ]),
                html.Td([
                    html.Button('search', id='search-button', n_clicks=0)
                ],style={'width':'10%'}),
                html.Td(style={'width':'5%'})
            ],style={'width':'50%'})
        ],style={'width':'100%', 'padding-left':'25%', 'padding-right':'25%'}),
    ],style={'width':'100%'}),
    html.Div([
        dcc.Slider(
            id='range-slider',
            min=1,
            max=400,
            step=None,
            value=31,
            marks={
                1:'1일',
                31:'1개월',
                92:'3개월',
                183:'6개월',
                275:'9개월',
                365:'12개월',
                400:'전체'
            }
        )
    ],style={'width':'50%','padding':5, 'padding-left':'25%', 'padding-right':'25%'}),
    html.Div(id='etf-info',children=[
        html.Div([
            html.H1(id='etf-name',style={'text-align':'center'})
        ]),
        html.Table([
            html.Td(style={'width':'10%'}),
            html.Td(id='etf-chart',style={'width':'50%'}),
            html.Td(style={'width':'5%'}),
            html.Td(id='etf-info-table',style={}),
            html.Td(style={'width':'25%'}),
        ],style={'width':'100%'}),
        html.Div(style={'height':20}),
        html.Table([
            html.Td(style={'width':'15%'}),
            html.Td(id='portfolio-table',style={'width':'40%'}),
            html.Td(style={'width':'10%'}),
            html.Td(id='portfolio-piechart',style={}),
            html.Td(style={'width':'15%'}),
        ],style={'width':'100%'}),
        html.Div(id='etf-history',style={'width':'70%', 'padding-left':'15%', 'padding-right':'15%'})
    ],style={'width':'100%'})
])

# 트렌드
trends = html.Div([
    dcc.Graph(
        id='etf-fluct-rate',
        figure=gd.get_tree_map()
    )
])

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
    ],style={'width':'100%'})
])

screener = None
compare = html.Div([
    html.Div(style={'height':'100'}),
    html.Div([
        html.Table([
            html.Tr([
                html.Td([
                    dcc.Dropdown(id='compare 1',
                        multi=False,
                        placeholder="ETF 1번",
                        value='',
                        style={'height':'30px','min_width':'100px','fontSize': 15,'textAlign': 'left'})
                ]),
                html.Td([
                    html.Button('비교하기', id='compare-button', n_clicks=0)
                ],style={'width':90}),
                html.Td([
                    dcc.Dropdown(id='compare 2',
                        multi=False,
                        placeholder="ETF 2번",
                        value='',
                        style={'height':'30px','min_width':'100px','fontSize': 15,'textAlign': 'left'})
                ]),
            ]),
        ],style={'width':'100%','textAlign': 'center'}),
    ],style={'width':'100%','textAlign': 'center'}),
    html.Div([
        dcc.RadioItems(
            id='compare-period',
            options=[
                {'label': '1주일', 'value': 7},
                {'label': '1개월', 'value': 31},
                {'label': '3개월', 'value': 92},
                {'label': '6개월', 'value': 183},
                {'label': '1년', 'value': 365},
                {'label': '3년', 'value': 1095},
                {'label': '5년', 'value': 1825}
            ],
            value=30,
            labelStyle={'display': 'inline-block'},style={'padding':'10px','textalign':'center'}
        ),
    ],style={'width':'100%','text-align':'center'}),

    html.Div([
        html.Div(id='compare-chart',style={'width':'100%','height':400}),
    ],style={'width':'80%','padding-left':'15%', 'padding-right':'5%'}),

    html.Div([
        html.Table([
            html.Td(style={'width':'20%'}),
            html.Td(id='compare-table'),
            html.Td(style={'width':'20%'}),
        ],style={'width':'100%','textalign':'center'})
    ],style={'width':'100%'})
],style={'width':'100%'})

# portfolio = html.Div([
#     html.Table([
#         html.Td([
#             html.Table([
#                 html.Tr([
#                     html.Td([
#                         dcc.Dropdown(id='portfolio-etfs-1',
#                             multi=True,
#                             placeholder="ETF 종목명을 입력하세요.",
#                             value='',
#                             style={'fontSize': 15})
#                     ],style={'width':'100%'}),
#                     html.Td([
#                         dcc.Input(id='input1', value='initial value', type='number')
#                     ]),
#                 ]),
#                 html.Tr([
#                     html.Td([
#                         dcc.Dropdown(id='portfolio-etfs-2',
#                             multi=True,
#                             placeholder="ETF 종목명을 입력하세요.",
#                             value='',
#                             style={'fontSize': 15})
#                     ],style={'width':'100%'}),
#                     html.Td([
#                         dcc.Input(id='input2', value='initial value', type='number')
#                     ]),
#                 ]),
#                 html.Tr([
#                     html.Td([
#                         dcc.Dropdown(id='portfolio-etfs-3',
#                             multi=True,
#                             placeholder="ETF 종목명을 입력하세요.",
#                             value='',
#                             style={'fontSize': 15})
#                     ],style={'width':'100%'}),
#                     html.Td([
#                         dcc.Input(id='input3', value='initial value', type='number')
#                     ]),
#                 ]),
#                 html.Tr([
#                     html.Td([
#                         dcc.Dropdown(id='portfolio-etfs-4',
#                             multi=True,
#                             placeholder="ETF 종목명을 입력하세요.",
#                             value='',
#                             style={'fontSize': 15}),
#                     ],style={'width':'100%'}),
#                     html.Td([
#                         dcc.Input(id='input4', value='initial value', type='number')
#                     ]),
#                 ]),
#                 html.Tr([
#                     html.Td([
#                         dcc.Dropdown(id='portfolio-etfs-5',
#                             multi=True,
#                             placeholder="ETF 종목명을 입력하세요.",
#                             value='',
#                             style={'fontSize': 15})
#                     ],style={'width':'100%'}),
#                     html.Td([
#                         dcc.Input(id='input5', value='initial value', type='number')
#                     ],style={'width':10}),
#                 ]),
#             ],style={'width':'100%'})
#         ],style={'width':'30%'}),
#         html.Td([
#             html.Tr([

#             ]),
#             html.Tr([

#             ])
#         ],style={'width':'70%'})
#     ],style={'width':'100%'})
# ],style={'width':'100%'})