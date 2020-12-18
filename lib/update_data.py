import pandas as pd
import json
import pymysql
from datetime import datetime, timedelta
import time
import json

from pykrx import stock
import FinanceDataReader as fdr
from sqlalchemy import create_engine
import getfromDB
import requests
from bs4 import BeautifulSoup

# etf 정보 크롤링 from naver
def get_etf_info(Symbol):
    url = "https://finance.naver.com/item/coinfo.nhn?code="+Symbol
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")

    # 가격정보
    price = bs_obj.find('dl', {'class': 'blind'}).find_all('dd')
    now_price = int(price[3].text.split()[1].replace(',','')) #현재가
    ex_price = int(price[4].text.split()[-1].replace(',','')) #전일종가

    # 상장주식수
    no_today = bs_obj.find("div", {"class": "first"})
    listed_shares = int(no_today.find_all("em")[1].text.replace(',',''))

    # 기초정보 부분
    base_info = bs_obj.find("table",{"class":"tbl_type1"})
    base_sub_info = base_info.find_all('span')

    # 상세정보
    base_index = base_sub_info[0].text # 기초지수
    etype = base_sub_info[1].text.split(', ') #유형
    type1 = etype[0]
    if len(etype)==2:
        type2 = etype[1]
    else:
        type2 = '일반'
    listed_day = base_info.find_all('td')[-1].text #상장일
    commission = float(bs_obj.find("table",{"summary":"펀드보수 정보"}).find('em').text[:-1]) # 수수료

    # 시가총액
    market_cap = now_price*listed_shares

    # 전일대비 상승률
    yield_from_ex = round((now_price - ex_price) / ex_price * 100, 2)

    print(now_price, ex_price, yield_from_ex, market_cap, listed_shares, commission, base_index, type1, type2, listed_day)
    return now_price, ex_price, yield_from_ex, market_cap, listed_shares, commission, base_index, type1, type2, listed_day

# etf 종목별 주가 히스토리 수집
def get_stock_prices(Symbol, last_update, today, conn):
    try:
        print(Symbol)
        start = datetime.strftime(datetime.strptime(last_update,'%Y%m%d') + timedelta(days=1), '%Y%m%d')
        stock_df = stock.get_etf_ohlcv_by_date(start, today, Symbol)
        stock_df.to_sql(name=Symbol, con=conn, if_exists='append', index=True)
    except:
        print(Symbol+':데이터 불러오기 실패', end= ' ')

# 실시간 세계 지수 크롤링 from yahoo finance
def get_world_indice_data(conn):
    df_list = pd.read_html('https://finance.yahoo.com/world-indices/')
    majorStockIdx = df_list[0][:-1]
    country_code = ['USA','USA','USA','USA','USA','GBR','USA','USA','GBR','DEU',
    'FRA','EU','EU','BEL','RUS','JPY','HKG','CHN','CHN','SGP',
    'AUS','AUS','IND','IDN','MYS','NZL','KOR','CHN','CAN','BRA','MEX','ESP','ARG','ISR','EGY']
    country_dict = {'USA':'미국','GBR':'영국','DEU':'벨기에','FRA':'프랑스','EU':'유럽','BEL':'벨기에','RUS':'러시아',
                    'JPY':'일본','HKG':'홍콩','CHN':'중국','SGP':'싱가포르','AUS':'호주','IND':'인도','IDN':'인도네시아',
                    'MYS':'말레이시아','NZL':'뉴질랜드','KOR':'대한민국','CAN':'캐나다','BRA':'브라질','MEX':'멕시코',
                    'ESP':'스페인','ARG':'아르헨티나','ISR':'이스라엘','EGY':'이집트'}
    majorStockIdx['Code'] = country_code
    majorStockIdx['Country'] = majorStockIdx['Code'].map(country_dict)
    majorStockIdx = majorStockIdx[['Symbol','Name','Country','Code','Last Price','Change','% Change']]
    majorStockIdx.to_sql(name='indices', con=conn, if_exists='replace', index=False)
    print('...지수 데이터 수집 완료')

# 포트폴리오 데이터 수집
def get_portfolio_data(symbols, num_symbols, conn):
    count = 1

    for symbol in symbols:
        print("{} {}/{}".format(symbol, count, num_symbols))
        try:
            portfolio = stock.get_etf_portfolio_deposit_file(symbol)
            portfolio.reset_index(inplace=True)
            portfolio.to_sql(name=symbol+'_pf', con=conn, if_exists='replace', index=False)
            count+=1
        except:
            print(symbol,'데이터 수집 불가')

# config 파일 저장
def save_config(config):
    with open('../config.json','w') as outfile:
        json.dump(config, outfile, indent='\t')


if __name__=='__main__':    
    with open('config.json', 'r') as f:
        config = json.load(f)

    HOSTNAME = config["MYSQL_INFO"]['HOSTNAME']
    PORT     = config["MYSQL_INFO"]['PORT']
    USERNAME = config["MYSQL_INFO"]['USERNAME']
    PASSWORD = config["MYSQL_INFO"]['PASSWORD']
    DATABASE = config["MYSQL_INFO"]['DATABASE']
    CHARSET1 = config["MYSQL_INFO"]['CHARSET1']    # MySQL에서 사용할 캐릭터셋 이름
    CHARSET2 = config["MYSQL_INFO"]['CHARSET2']    # Python에서 사용할 캐릭터셋 이름

    # 데이터베이스 포맷 설정
    con_str_fmt = "mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset={5}"
    con_str = con_str_fmt.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE, CHARSET1)
    pymysql.install_as_MySQLdb()

    # mysql과 연결
    import MySQLdb
    engine = create_engine(con_str, encoding=CHARSET2)
    conn = engine.connect()
    print('...데이터베이스 연결 완료')

    # 한국 etf 리스트 저장
    etf_info = fdr.EtfListing('KR')
    etf_info = pd.DataFrame(etf_info, columns=['Symbol','Name','now_price','ex_price',
                                                'yield_from_ex','market_cap','listed_shares',
                                                'commission','base_index','type1','type2','listed_day'])

    # etf 정보 dataframe
    print('...ETF 정보 수집중')
    for idx in range(len(etf_info)):
        Symbol = etf_info.loc[idx,'Symbol']
        print(Symbol, end=' ')
        etf_info.loc[idx,'now_price':'listed_day'] = get_etf_info(Symbol)

    etf_info.to_sql(name='etfList', con=conn, if_exists='replace', index=False)
    print('...ETF 정보 리스트 저장 완료')

    # 종목별 주가 데이터 저장
    print('...주가 데이터 저장 중')
    today = datetime.today().strftime('%Y%m%d')
    last_update = config['LAST_UPDATE']
    for Symbol in etf_info['Symbol']:
        get_stock_prices(Symbol, last_update, today, conn)
    print('...주가 데이터 저장 완료')

    # 주요 지수 데이터 저장
    print('...주요 지수 데이터 저장 중')
    for indice in ['KS11','KQ11', 'DJI', 'US500', 'IXIC']:
        indice_df = fdr.DataReader(indice, '2015-01-01')
        indice_df.to_sql(name=indice, con=conn, if_exists='replace', index=True)
        print('추가완료...',indice)
    print('...주요 지수 데이터 저장 완료')

    # 세계 지수 데이터 저장
    print('...세계 지수 데이터 저장 중')
    get_world_indice_data(conn)
    print('...세계 지수 데이터 저장 완료')

    # 포트폴리오 데이터 저장
    print('...포트폴리오 데이터 수집 중')
    symbols = etf_info['Symbol']
    num_symbols = len(symbols)
    get_portfolio_data(symbols, num_symbols, conn)
    print('...포트폴리오 데이터 수집 완료')


    config['LAST_UPDATE'] = today
    save_config(config)