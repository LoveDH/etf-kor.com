import pandas as pd
from datetime import datetime
import time
from tqdm.notebook import tqdm

import FinanceDataReader as fdr
from pykrx import stock
import pymysql
from sqlalchemy import create_engine

HOSTNAME = "localhost"
PORT     = 3306
USERNAME = "lovedh"
PASSWORD = "123"
DATABASE = "etfkor"
CHARSET1  = "utf8"     # MySQL에서 사용할 캐릭터셋 이름
CHARSET2  = "utf-8"    # Python에서 사용할 캐릭터셋 이름

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
etf_list = fdr.EtfListing('KR')

etf_list.to_sql(name='etfList', con=conn, if_exists='replace', index=False)
print('...ETF 리스트 저장 완료')

# 종목별 주가 데이터 저장
today = datetime.today().strftime('%Y%m%d')
for ticker in etf_list['Symbol']:
    try:
        print(ticker, end=' ')
        df = stock.get_etf_ohlcv_by_date("20020101", today, ticker)
        df.to_sql(name=ticker, con=conn, if_exists='replace', index=True)
    except:
        print(ticker+':데이터 불러오기 실패', end= ' ')
print('...주가 데이터 저장 완료')