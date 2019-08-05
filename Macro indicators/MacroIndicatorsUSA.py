import pandas as pd
from dataapi import FRED
import datetime
from datetime import date
from sklearn import preprocessing
import numpy as np
import requests
from bloomberg import BBG
from sklearn import preprocessing
import matplotlib.pyplot as plt
from scipy.stats import zscore

bbg = BBG()
getdata = FRED()
min_max_scaler = preprocessing.MinMaxScaler()

# Initial and End Dates

start_date = pd.to_datetime('01-jan-2000')
end_date = pd.to_datetime('15-jun-2019')

### GROWTH SERIES

#fetching US Conference Board Consumer Confidence SA 1985=100
#   Original Date: '28-fev-1967'

df = bbg.fetch_series(securities=['CONCCONF Index'],
                      fields=['PX_LAST'],
                      startdate=start_date,
                      enddate=end_date)

concconf = pd.DataFrame(data=df)
concconf = concconf.droplevel(0)
concconf = concconf.reset_index()
concconf = concconf.set_index('TRADE_DATE')
concconf.index.names = ['Date']
concconf = concconf.resample('Q').mean()

#normalizing series Consumer Confidence

x = np.array(concconf['CONCCONF Index'])
x = x.reshape(-1,1)
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
confnorm = concconf
confnorm['CONCCONF Normalized'] = ''
confnorm['CONCCONF Normalized'] = x_scaled
confnorm = confnorm.drop('CONCCONF Index', axis=1)

#fetching GDP
df_gr = pd.DataFrame(getdata.fetch("GDPC1", start_date, end_date))
df_gr = df_gr['GDPC1'].resample('Q').mean()
df_gr = df_gr.pct_change(4)
df_gr = df_gr.dropna()

#normalizing GDP
x = df_gr.values
x = x.reshape(-1,1)
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df_gr_norm = pd.DataFrame(x_scaled, index=df_gr.index, columns=['GDP Growth Normalized'])

#fetching potential GDP until today's date
df_expectedgr = pd.DataFrame(getdata.fetch("GDPPOT", start_date, end_date))
df_expectedgr = df_expectedgr['GDPPOT'].resample('Q').mean()
df_expectedgr = df_expectedgr.pct_change(4)
df_expectedgr = df_expectedgr.dropna()

#normalizing potential GDP
y = df_expectedgr.values
y = y.reshape(-1,1)
y_scaled = min_max_scaler.fit_transform(y)
df_expectedgr_norm = pd.DataFrame(y_scaled, index=df_expectedgr.index, columns=['POTGDP Normalized'])

#fetching CFNAI
df_CFNAI = pd.DataFrame(getdata.fetch("CFNAI", start_date, end_date))
df_CFNAI = df_CFNAI.resample('Q').mean()
df_CFNAI = df_CFNAI.dropna()

#normalizing CFNAI
w = df_CFNAI.values
w = w.reshape(-1,1)
w_scaled = min_max_scaler.fit_transform(w)
df_CFNAI_norm = pd.DataFrame(w_scaled, index=df_CFNAI.index, columns=['CFNAI Normalized'])

#fetching real earnings
df_realear = getdata.fetch("LES1252881600Q", start_date, end_date)
df_realear = df_realear['LES1252881600Q'].resample("Q").mean()
df_realear = df_realear.pct_change(4)
df_realear = df_realear.dropna()

#normalizing real earnings
a = df_realear.values
a = a.reshape(-1,1)
a_scaled = min_max_scaler.fit_transform(a)
df_realear_norm = pd.DataFrame(a_scaled, index=df_realear.index, columns=['Real Earnings Normalized'])

#merging DataFrames

df_realgr = pd.merge(df_expectedgr_norm,df_gr_norm, on='Date', how='outer')

df_realgr = pd.merge(df_realgr,df_realear_norm, on='Date', how='outer')

df_realgr = pd.merge(df_realgr,df_CFNAI_norm, on='Date', how='outer')

df_realgr = pd.merge(df_realgr,confnorm, on='Date', how='outer')


ax = plt.gca()
df_realgr.plot(kind='line', y='Real Earnings Normalized', color='blue', ax=ax)
df_realgr.plot(kind='line', y='CFNAI Normalized', color='green', ax=ax)
df_realgr.plot(kind='line', y='POTGDP Normalized', color='red', ax=ax)
df_realgr.plot(kind='line', y='GDP Growth Normalized', color='purple', ax=ax)
df_realgr.plot(kind='line', y='CONCCONF Normalized', color='gray', ax=ax)
#plt.show()

#adding a column with average

df_realgr["Real Growth"] = df_realgr.mean(numeric_only = True, axis=1)
#print(df_realgr)

## VOLATILITY SERIES

#fetching S&P index and general US 10-year bonds volatility
#   Original Date: '28-fev-1967'

df = bbg.fetch_series(securities=['SPX Index', 'USGG10YR Index'],
                      fields=['VOLATILITY_90D', 'Volatil 90D'],
                      startdate=start_date,
                      enddate=end_date)

volSPX_90 = pd.DataFrame(data=df['SPX Index'])
volSPX_90 = volSPX_90.droplevel('FIELD')
volSPX_90 = volSPX_90.resample('Q').last()
volbonds_90 = pd.DataFrame(data=df['USGG10YR Index'])
volbonds_90 = volbonds_90.droplevel('FIELD')
volbonds_90 = volbonds_90.resample('Q').last()

#plot series
#ax = plt.gca()
#volSPX_90.plot(kind='line', color='blue', ax=ax)
#volbonds_90.plot(kind='line', color='red', ax=ax)
#plt.show()

#normalizing series SPX and US Bonds
x = np.array(volSPX_90['SPX Index'])
x = x.reshape(-1,1)
spxnorm = min_max_scaler.fit_transform(x)
y = np.array(volbonds_90['USGG10YR Index'])
y = y.reshape(-1,1)
bondsnorm = min_max_scaler.fit_transform(y)
volUS = volSPX_90
volUS['SPX Index Normalized'] = ''
volUS['SPX Index Normalized'] = spxnorm
volUS['Bonds Vol. Normalized'] = ''
volUS['Bonds Vol. Normalized'] = bondsnorm
volUS = volUS.drop('SPX Index', axis=1)

#plotting normalized series
#ax = plt.gca()
#volUS.plot(kind='line', y='SPX Index Normalized', color='blue', ax=ax)
#volUS.plot(kind='line', y='Bonds Vol. Normalized', color='red', ax=ax)
#plt.show()

#average volatility
AvgVolUS = volUS
AvgVolUS['Avg Vol US'] = ''
AvgVolUS['Avg Vol US'] = volUS.mean(numeric_only = True, axis=1)
AvgVolUS.index.names = ['Date']
AvgVolUS = AvgVolUS.drop('Bonds Vol. Normalized', axis=1)


## INFLATION SERIES

#fetching CPI
df_cpi = pd.DataFrame(getdata.fetch("CPIAUCSL", start_date, end_date))
df_cpi = pd.DataFrame(df_cpi["CPIAUCSL"].resample('Q').mean())

#normalizing CPI
b = df_cpi.values
b = b.reshape(-1, 1)
min_max_scaler = preprocessing.MinMaxScaler()
b_scaled = min_max_scaler.fit_transform(b)
df_cpi_norm = pd.DataFrame(b_scaled, index=df_cpi.index, columns=['CPI Normalized'])

#CPI growth
df_cpigr = df_cpi.pct_change(4)
df_cpigr = df_cpigr.dropna()
df_cpigr = df_cpigr['CPIAUCSL'].resample('Q').mean()

#normalizing CPI growth
c = df_cpigr.values
c = c.reshape(-1, 1)
c_scaled = min_max_scaler.fit_transform(c)
df_cpigr_norm = pd.DataFrame(c_scaled, index=df_cpigr.index, columns=['CPI Growth Normalized'])

#fetching GDP deflator
df_gdpdef = pd.DataFrame(getdata.fetch("GDPDEF", start_date, end_date))
df_gdpdef = df_gdpdef['GDPDEF'].resample('Q').mean()
df_gdpdef = df_gdpdef.pct_change(4)
df_gdpdef = df_gdpdef.dropna()

#normalizing GDP deflator
d = df_gdpdef.values
d = d.reshape(-1, 1)
d_scaled = min_max_scaler.fit_transform(d)
df_gdpdef_norm = pd.DataFrame(d_scaled, index=df_gdpdef.index, columns=['GDP Deflator Normalized'])

#merging DataFrames

df_inf = pd.merge(df_cpi_norm,df_cpigr_norm, on='Date', how='outer')
df_inf = pd.merge(df_inf,df_gdpdef_norm, on='Date', how='outer')

#calculating average inflation

df_inf["inflation"] = df_inf.mean(numeric_only=True, axis=1)
#print(df_inf)

## MERGING GROWTH, VOLATILITY AND INFLATION DATAFRAMES

df_growth = df_realgr["Real Growth"]
df_vol = AvgVolUS['Avg Vol US']
df_series = df_inf["inflation"]
df_series = pd.merge(df_series, df_growth, on="Date", how="outer")
df_series = pd.merge(df_series, df_vol, on="Date", how="outer")
df_series = df_series.apply(zscore)
#print(df_series)

#plotting Data Frames
ax = plt.gca()
df_series.plot(kind='line', y='Real Growth', color='blue', ax=ax)
df_series.plot(kind='line', y='Avg Vol US', color='green', ax=ax)
df_series.plot(kind='line', y='inflation', color='red', ax=ax)
plt.axhline(y=0, color='black', linestyle='-')
#plt.show()

#data classification

clas_df = df_series
clas_df['Inflation Cycle'] = np.where(clas_df['inflation']>0, "Inflationary", "Disinflationary")
clas_df['Growth Cycle'] = np.where(clas_df['Real Growth']>0, "Boom", "Stagnation")
clas_df['Cycle']= clas_df['Inflation Cycle'] + ' ' + clas_df['Growth Cycle']

clas_df['infcy'] = np.where(clas_df['inflation']>0, 1, 0)
clas_df['cy'] = np.where(clas_df['Real Growth']>0, 2, 0)
clas_df['cy'] = clas_df['infcy'] + clas_df['cy']
clas_df['Cycle Change'] = clas_df['cy'].diff()
cycle = []
cycle = clas_df['Cycle Change'].loc[clas_df['Cycle Change'] != 0]
print(cycle)
