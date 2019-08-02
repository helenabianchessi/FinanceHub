from dataapi import SGS
from bloomberg import BBG
import numpy as np
import pandas as pd
from sklearn import preprocessing

getdata = SGS()
bbg = BBG()

start_date = pd.to_datetime("01-01-2001")
end_date = pd.to_datetime("07-01-2019")

#fetching Brazil FGV Consumer Confidence Index SA Sep 2005=100 Original Date: '30-sep-2005'

df = bbg.fetch_series(securities=['BZFGCCSA Index'],
                      fields=['PX_LAST'],
                      startdate=start_date,
                      enddate=end_date)

consbr = pd.DataFrame(data=df)
consbr = consbr.droplevel(0)
consbr = consbr.reset_index()
consbr = consbr.set_index('TRADE_DATE')
consbr = consbr.resample('Q').mean()

# Normalized series Consumer Confidence

x = np.array(consbr['BZFGCCSA Index'])
x = x.reshape(-1,1)
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)

consbrnorm = consbr
consbrnorm['BZFGCCSA Normalized'] = ''
consbrnorm['BZFGCCSA Normalized'] = x_scaled
consbrnorm = consbrnorm.drop('BZFGCCSA Index', axis=1)

#fetching GDP Growth in R$
df_gr = pd.DataFrame(getdata.fetch("1207",start_date, end_date)) #for GDP in dollars, change the string to 7324
df_gr = df_gr['1207'].resample('Q').mean()
df_gr = df_gr.pct_change(4)
df_gr = df_gr.dropna()

#normalizing GDP
x = df_gr.values
x = x.reshape(-1,1)
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df_gr_norm = pd.DataFrame(x_scaled, index=df_gr.index, columns=['GDP Growth Normalized'])

#fetching real earnings
df_realear = getdata.fetch("10790",start_date, end_date)
df_realear = df_realear['10790'].resample("Q").mean()
df_realear = df_realear.pct_change(4)
df_realear = df_realear.dropna()

#normalizing real earnings
a = df_realear.values
a = a.reshape(-1,1)
a_scaled = min_max_scaler.fit_transform(a)
df_realear_norm = pd.DataFrame(a_scaled, index=df_realear.index, columns=['Real Earnings Normalized'])
print(df_gr_norm)

#fetching IPCA
df_cpi = pd.DataFrame(getdata.fetch("433", start_date, end_date))
df_cpi = pd.DataFrame(df_cpi["433"].resample('Q').mean())

#normalizing IPCA
b = df_cpi.values
b = b.reshape(-1, 1)
min_max_scaler = preprocessing.MinMaxScaler()
b_scaled = min_max_scaler.fit_transform(b)
df_cpi_norm = pd.DataFrame(b_scaled, index=df_cpi.index, columns=['CPI Normalized'])

#IPCA growth
df_cpigr = df_cpi.pct_change(4)
df_cpigr = df_cpigr.dropna()
df_cpigr = df_cpigr['433'].resample('Q').mean()

#normalizing IPCA growth
c = df_cpigr.values
c = c.reshape(-1, 1)
c_scaled = min_max_scaler.fit_transform(c)
df_cpigr_norm = pd.DataFrame(c_scaled, index=df_cpigr.index, columns=['CPI Growth Normalized'])

#fetching GDP deflator
df_gdpdef = pd.DataFrame(getdata.fetch("1211"))
df_gdpdef = df_gdpdef.dropna()

#normalizing GDP deflator
d = df_gdpdef.values
d = d.reshape(-1, 1)
d_scaled = min_max_scaler.fit_transform(d)
df_gdpdef_norm = pd.DataFrame(d_scaled, index=df_gdpdef.index, columns=['GDP Deflator Normalized'])

#Merging DataFrames#

df_inf = pd.merge(df_cpi_norm,df_cpigr_norm, on='Date', how='outer')

df_inf = pd.merge(df_inf,df_gdpdef_norm, on='Date', how='outer')

#calculating average inflation

df_inf["inflation"] = df_inf.mean(numeric_only=True, axis=1)

print(df_inf)