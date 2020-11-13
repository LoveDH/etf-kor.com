from pykrx import stock

df = stock.get_etf_portfolio_deposit_file('069500')
print(df)