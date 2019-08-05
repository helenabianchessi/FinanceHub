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

confnorm = consbr
confnorm['BZFGCCSA Normalized'] = ''
confnorm['BZFGCCSA Normalized'] = x_scaled
confnorm = confnorm.drop('BZFGCCSA Index', axis=1)

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

#Merging Real Growth DataFrames#

df_realgr = pd.merge(df_gr_norm,df_realear_norm, on='Date', how='outer')

df_realgr = pd.merge(df_realgr,confnorm, on='Date', how='outer')

#adding a column with average

df_realgr["Real Growth"] = df_realgr.mean(numeric_only = True, axis=1)

# VOLATILITY SERIES

start_date = pd.to_datetime('01-jan-2010')
end_date = pd.to_datetime('today')

df = bbg.fetch_series(securities=['IBOV Index', 'GEBR10Y Index'],
                      fields=['VOLATILITY_90D', 'Volatil 90D'],
                      startdate=start_date,
                      enddate=end_date)

volIBOV_90 = pd.DataFrame(data=df['IBOV Index'])
volIBOV_90 = volIBOV_90.droplevel('FIELD')
volIBOV_90 = volIBOV_90.resample('Q').last()
voltitul_90 = pd.DataFrame(data=df['GEBR10Y Index'])
voltitul_90 = voltitul_90.droplevel('FIELD')
voltitul_90 = voltitul_90.resample('Q').last()

# Normalized series IBOV and BR Bonds (titulos)
x = np.array(volIBOV_90['IBOV Index'])
x = x.reshape(-1,1)
ibovnorm = min_max_scaler.fit_transform (x)
y = np.array(voltitul_90['GEBR10Y Index'])
y = y.reshape(-1,1)
titulnorm = min_max_scaler.fit_transform(y)
volBR = volIBOV_90
volBR['IBOV Index Normalized'] = ''
volBR['IBOV Index Normalized'] = ibovnorm
volBR['Titulos Vol. Normalized'] = ''
volBR['Titulos Vol. Normalized'] = titulnorm
volBR = volBR.drop('IBOV Index', axis=1)

# Average Volatility

AvgVolBR = volBR
AvgVolBR['Avg Vol Br'] = ''
AvgVolBR['Avg Vol BR'] = volBR.mean(numeric_only = True, axis=1)
AvgVolBR = AvgVolBR.drop('Titulos Vol. Normalized', axis=1)

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

# MERGING GROWTH, VOLATILITY AND INFLATION DATAFRAMES

df_growth = df_realgr["Real Growth"]
df_vol = AvgVolBR['Avg Vol BR']
df_series = df_inf["inflation"]
df_series = pd.merge(df_series, df_growth, on="Date", how="outer")
df_series = pd.merge(df_series, df_vol, on="Date", how="outer")
df_series = df_series.apply(zscore)
print(df_series)

# Data Classification

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
