import dash

# 기존에 구현되어있는 css 소스 사용 -> 추후 수정 예정
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)