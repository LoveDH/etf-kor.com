# etf-kor.com

[![ETF코리아](./assets/logo.png)](https://github.com/LoveDH/etf-kor.com/)

## 요약

&nbsp;코로나19 바이러스 확산으로 인해 세계 경제가 침체하고 제로금리 시대가 오면서 투자는 이제 선택이 아닌 필수인 시대가 도래했습니다. 주식 투자를 하는 개인이 폭발적으로 늘어나면서 2020년 초에는 ‘동학개미운동’이라는 말이 나올 정도였습니다. 하지만 그 속에는 주식을 처음 투자해보는 초보투자자들이 많습니다. 
  
&nbsp;**ETF**는 **해당 투자자가 설정한 목표에 따라 투자를 할 수 있도록 다양한 종류로 구성이 되어있고, 집중투자뿐만 아니라 분산투자의 효과 또한 가지고 있어 안정적이면서도 고수익을 노려볼 수 있는 상품**입니다. 따라서 종목을 선택하는 능력이 부족한 개인 투자자들에게 점점 인기를 얻고 있으며 그 시장규모도 기하급수적으로 증가하고 있습니다. 
  
&nbsp;해외 거래소(특히 뉴욕 거래소)에 상장된 ETF들은 [etf.com](, etfdb.com 등의 전문 사이트에서 차트, 구성 종목, 분석내용 등 관련 정보를 자세히 찾아볼 수 있으나, 현재 한국거래소에 상장된 ETF를 전문적으로 다룬 사이트는 없는 실정입니다. 네이버, 다음 등의 포털사이트에서 증권시장에 대한 정보를 얻을 수 있지만, 시각화가 잘 되어있지 않아 초보자는 시장 동향을 파악하기 힘든 상황다.

&nbsp;본 프로젝트로 개발한 웹 대시보드를 통해 많은 사용자들이 ETF 투자에 관심을 가지고, 건전한 투자 의식을 함양하기를 소망합니다.


## 개발 및 실행 환경
- Ubuntu 16.04
- Miniconda virtual environment
- MySQL

## 라이브러리
- `plotly`
- `dash==1.17.0`
- `pykrx`
- `finance-datareader`
- `SQLAlchemy`
- `PyMySQL`
- `bs4`, `beautifulsoup4`
- `numpy`, `pandas`

## 폴더 구조
```
├── app.py : 서버 실행 파일
├── assets : css, 이미지 등을 저장하는 폴더 
├── config.json : 데이터베이스 정보 및 날짜 저장
├── lib
│   ├── getfromDB.py : 데이터를 이용해 그래프 생성
│   ├── pages.py : 페이지 레이아웃
│   └── update_data.py : 현재 데이터 불러오기
├── README.md
├── requirements.txt : 필요한 패키지
└── source : 그래프 소스가 담겨있는 폴더(실행과 상관없음)
```

## 실행법
> 실행 전 Mysql 데이터베이스 세팅 및 configure에 정보 입력
```
pip install -r requirements.txt
```
```
# 초기 데이터 수집
python lib/initial_data_collect.py
```
```
# 서버 실행
python app.py
```
