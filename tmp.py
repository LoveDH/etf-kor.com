import FinanceDataReader as fdr
import pandas as pd
import json
from sqlalchemy import create_engine
import pymysql
from pykrx import stock

with open('config.json', 'r') as f:
    config = json.load(f)

HOSTNAME = config["MYSQL_INFO"]['HOSTNAME']
PORT     = config["MYSQL_INFO"]['PORT']
USERNAME = config["MYSQL_INFO"]['USERNAME']
PASSWORD = config["MYSQL_INFO"]['PASSWORD']
DATABASE = config["MYSQL_INFO"]['DATABASE']
CHARSET1 = config["MYSQL_INFO"]['CHARSET1']    # MySQL에서 사용할 캐릭터셋 이름
CHARSET2 = config["MYSQL_INFO"]['CHARSET2']    # Python에서 사용할 캐릭터셋 이름

def get_data_from_db(sql):
    connection = pymysql.connect(
        host=HOSTNAME,
        user=USERNAME,
        password=PASSWORD,
        db=DATABASE,
        charset=CHARSET1)
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()

    return data
sql = "select 종목, 계약수, 금액, 비중 from etfkor.069500_pf"
df = pd.DataFrame(get_data_from_db(sql),columns=['종목','계약수','금액','비중'])