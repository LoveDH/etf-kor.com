import FinanceDataReader as fdr

df_krx = fdr.StockListing('KRX')
print(list(df_krx))

df_nasdaq = fdr.StockListing('NASDAQ')
print(list(df_nasdaq))

print(df_krx['Sector'].unique(),'\n')
print(df_krx['Industry'].unique(),'\n')
print(df_nasdaq['Industry'].unique())
print(set(df_krx['Sector']) & set(df_nasdaq['Industry']))
