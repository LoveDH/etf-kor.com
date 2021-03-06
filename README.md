# 한국 ETF 대시보드 개발 프로젝트 (개발중)
[![ETF코리아](./assets/logo.png)](https://github.com/LoveDH/etf-kor.com/)

<p align="center">
  <img width="49%" src="https://user-images.githubusercontent.com/44254662/110760356-f8256080-8291-11eb-8ffc-a98dad806bcc.gif" />
  <img width="49%" src="https://user-images.githubusercontent.com/44254662/110760372-fe1b4180-8291-11eb-9fe6-2458f7253359.gif" />
</p>

<p align="center">
  <img width="32%" src="https://user-images.githubusercontent.com/44254662/110760369-fc517e00-8291-11eb-889b-23e991888e5c.gif" />
  <img width="32%" src="https://user-images.githubusercontent.com/44254662/110760362-f9ef2400-8291-11eb-866f-ba3eee42b92a.gif" />
  <img width="32%" src="https://user-images.githubusercontent.com/44254662/110760349-f65b9d00-8291-11eb-8f99-3f61d2b49c54.gif" />
</p>


## 개요

&nbsp;코로나19 바이러스 확산으로 인해 세계 경제가 침체하고 제로금리 시대가 오면서 투자는 이제 선택이 아닌 필수인 시대가 도래했습니다. 주식 투자를 하는 개인이 폭발적으로 늘어나면서 2020년 초에는 ‘동학개미운동’이라는 말이 나올 정도였습니다. 하지만 그 속에는 주식을 처음 투자해보는 초보투자자들이 많습니다. 
  
&nbsp;**ETF**는 **해당 투자자가 설정한 목표에 따라 투자를 할 수 있도록 다양한 종류로 구성이 되어있고, 집중투자뿐만 아니라 분산투자의 효과 또한 가지고 있어 안정적이면서도 고수익을 노려볼 수 있는 상품**입니다. 따라서 종목을 선택하는 능력이 부족한 개인 투자자들에게 점점 인기를 얻고 있으며 그 시장규모도 기하급수적으로 증가하고 있습니다. 
  
&nbsp;해외 거래소(특히 뉴욕 거래소)에 상장된 ETF들은 [etf.com](https://www.etf.com/), [etfdb.com](https://etfdb.com/) 등의 전문 사이트에서 차트, 구성 종목, 분석내용 등 관련 정보를 자세히 찾아볼 수 있으나, 현재 **한국거래소에 상장된 ETF를 전문적으로 다룬 사이트는 없는 실정**입니다. 네이버, 다음 등의 포털사이트에서 증권시장에 대한 정보를 얻을 수 있지만, 시각화가 잘 되어있지 않아 초보자는 시장 동향을 파악하기 힘든 상황입니다.

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
├── README.md
├── app.py : dash 앱 정의파일
├── assets : css, 이미지 등을 저장하는 폴더 
├── callbacks.py : 콜백 함수 정의
├── config.json : 데이터베이스 정보 및 날짜 저장
├── index.py : 메인 화면 및 실행파일
├── lib
│   ├── getfromDB.py : 데이터를 이용해 그래프 생성
│   ├── pages.py : 페이지 레이아웃
│   └── update_data.py : 데이터 업데이트
├── requirements.txt : 필요한 패키지
```

## 실행 방법
> 실행 전 Mysql 데이터베이스 세팅 및 configure에 정보 입력
```
pip install -r requirements.txt
```
```
# 초기 데이터 수집 및 데이터 
python lib/update_data.py
```
```
# 서버 실행
python index.py
```

#### PyMySQL을 통한 데이터베이스 연동 함수
```python
with open('config.json', 'r') as f:
    config = json.load(f)
    
HOSTNAME = config["MYSQL_INFO"]['HOSTNAME']
PORT     = config["MYSQL_INFO"]['PORT']
USERNAME = config["MYSQL_INFO"]['USERNAME']
PASSWORD = config["MYSQL_INFO"]['PASSWORD']
DATABASE = config["MYSQL_INFO"]['DATABASE']
CHARSET1 = config["MYSQL_INFO"]['CHARSET1']    # MySQL에서 사용할 캐릭터셋 이름
CHARSET2 = config["MYSQL_INFO"]['CHARSET2']    # Python에서 사용할 캐릭터셋 이름

# 적절한 sql문을 input으로 할당하면 해당 데이터베이스에서 sql을 실행한 결과값을 반환한다.
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
```

#### 추후 업데이트 계획
- **Home**
    - 미국 지수 추가 (NASDAQ, DOW)
- **Trend**
    - 기간 옵션 추가
- **Search**
    - 거래량, 이동평균선, 볼린저밴드 등 지표 추가
    - candle chart(일,주,연봉)와 Line chart(1일, 7일, 30일 ...)로 분리
    - 유사 종목 추천
- **기능 추가**
    - **Portfolio 탭 추가**:사용자별 희망 ETF를 본인 목록에 담아 예상 과거 수익률 및 종목 구성비율 표시 기능
    - **실시간 기능 추가**: 실시간 주가 데이터를 반영
    - **예측 기능 추가**: 머신러닝, 딥러닝 모델을 이용한 간단한 예측기능 
- **기타**
    - 섹터 세분화
