import pandas as pd
from datetime import datetime
import time
from tqdm.notebook import tqdm

import FinanceDataReader as fdr
from pykrx import stock
import pymysql
from sqlalchemy import create_engine
import requests
from bs4 import BeautifulSoup

HOSTNAME = "localhost"
PORT     = 3306
USERNAME = "lovedh"
PASSWORD = "123"
DATABASE = "etfkor"
CHARSET1  = "utf8"     # MySQL에서 사용할 캐릭터셋 이름
CHARSET2  = "utf-8"    # Python에서 사용할 캐릭터셋 이름


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
    etype = base_sub_info[1].text.replace(', ','-') #유형
    listed_day = base_info.find_all('td')[-1].text #상장일
    commission = bs_obj.find("table",{"summary":"펀드보수 정보"}).find('em').text # 수수료

    # 시가총액
    market_cap = now_price*listed_shares

    print(now_price, ex_price, market_cap, listed_shares, commission, base_index, etype, listed_day)
    return now_price, ex_price, market_cap, listed_shares, commission, base_index, etype, listed_day

def get_stock_prices(Symbol):
    global today



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
etf_info = pd.DataFrame(etf_info, columns=['Symbol','Name','now_price','ex_price','market_cap','listed_shares','commission','base_index','type','listed_day'])

today = datetime.today().strftime('%Y%m%d')
# 종목별 주가 데이터 저장
print('...주가 데이터 저장 중')
for Symbol in etf_info['Symbol']:
    try:
        print(Symbol, end=' ')
        stock_df = stock.get_etf_ohlcv_by_date("20020101", today, Symbol)
        stock_df.to_sql(name=Symbol, con=conn, if_exists='replace', index=True)
    except:
        print(Symbol+':데이터 불러오기 실패', end= ' ')
print('...주가 데이터 저장 완료')

# etf 정보 dataframe
print('...ETF 정보 수집중')
for idx in range(len(etf_info)):
    Symbol = etf_info.loc[idx,'Symbol']
    print(Symbol, end=' ')
    etf_info.loc[idx,'now_price':'listed_day'] = get_etf_info(Symbol)

etf_info.to_sql(name='etfList', con=conn, if_exists='replace', index=False)
print('...ETF 정보 리스트 저장 완료')