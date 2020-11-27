import pandas as pd
import json

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
print(majorStockIdx)
print(type(majorStockIdx))
