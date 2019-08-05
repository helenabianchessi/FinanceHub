from bloomberg import BBG
import pandas as pd

start_date = '30-mar-2015'
end_date = '30-mar-2019'

bbg = BBG()

# Grabs tickers and fields
df = bbg.fetch_series(securities=['PETR4'],
                      fields=['VOLATILITY_90D'],
                      startdate=start_date,
                      enddate=end_date)
print(df)
