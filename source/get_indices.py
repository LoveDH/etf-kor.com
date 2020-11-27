import pandas as pd
from datetime import datetime
import time
import json

import FinanceDataReader as fdr
import pymysql
from sqlalchemy import create_engine


with open('../config.json', 'r') as f:
    config = json.load(f)

HOSTNAME = config["MYSQL_INFO"]['HOSTNAME']
PORT     = config["MYSQL_INFO"]['PORT']
USERNAME = config["MYSQL_INFO"]['USERNAME']
PASSWORD = config["MYSQL_INFO"]['PASSWORD']
DATABASE = config["MYSQL_INFO"]['DATABASE']
CHARSET1 = config["MYSQL_INFO"]['CHARSET1']    # MySQL에서 사용할 캐릭터셋 이름
CHARSET2 = config["MYSQL_INFO"]['CHARSET2']    # Python에서 사용할 캐릭터셋 이름

today = datetime.today().strftime('%Y%m%d')

if __name__=='__main__':

    # 데이터베이스 포맷 설정
    con_str_fmt = "mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset={5}"
    con_str = con_str_fmt.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE, CHARSET1)
    pymysql.install_as_MySQLdb()

    # mysql과 연결
    import MySQLdb
    engine = create_engine(con_str, encoding=CHARSET2)
    conn = engine.connect()
    print('...데이터베이스 연결 완료')


    for indice in ['KS11','KQ11', 'DJI', 'US500', 'IXIC']:
        indice_df = fdr.DataReader(indice, '2015-01-01')
        indice_df.to_sql(name=indice, con=conn, if_exists='replace', index=True)
        print('추가완료...',indice)

