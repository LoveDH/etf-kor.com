import pandas as pd
import json
import pymysql
from pykrx import stock
from sqlalchemy import create_engine
import getfromDB

with open('config.json', 'r') as f:
    config = json.load(f)

HOSTNAME = config["MYSQL_INFO"]['HOSTNAME']
PORT     = config["MYSQL_INFO"]['PORT']
USERNAME = config["MYSQL_INFO"]['USERNAME']
PASSWORD = config["MYSQL_INFO"]['PASSWORD']
DATABASE = config["MYSQL_INFO"]['DATABASE']
CHARSET1 = config["MYSQL_INFO"]['CHARSET1']    # MySQL에서 사용할 캐릭터셋 이름
CHARSET2 = config["MYSQL_INFO"]['CHARSET2']    # Python에서 사용할 캐릭터셋 이름

con_str_fmt = "mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset={5}"
con_str = con_str_fmt.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE, CHARSET1)
pymysql.install_as_MySQLdb()

# mysql과 연결
import MySQLdb
engine = create_engine(con_str, encoding=CHARSET2)
conn = engine.connect()
print('...데이터베이스 연결 완료')

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

print('...포트폴리오 데이터 수집 중')
symbols = getfromDB.etflist['Symbol']
num_symbols = len(symbols)
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

        