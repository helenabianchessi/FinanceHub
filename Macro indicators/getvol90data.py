"""
Authors: Helena Bianchessi and Beatriz Jesus
"""
from bloomberg import BBG
import pandas as pd
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt

bbg = BBG()
min_max_scaler = preprocessing.MinMaxScaler()

# Pulling IBOVESPA and S&P indexes volatility, as well as general US and BR 10-year bonds
#   Original Date: '28-fev-1967'

start_date = pd.to_datetime('01-jan-2010')
end_date = pd.to_datetime('today')

df = bbg.fetch_series(securities=['SPX Index', 'IBOV Index', 'USGG10YR Index', 'GEBR10Y Index'],
                      fields=['VOLATILITY_90D', 'Volatil 90D'],
                      startdate=start_date,
                      enddate=end_date)

volSPX_90 = pd.DataFrame(data=df['SPX Index'])
volSPX_90 = volSPX_90.droplevel('FIELD')
volSPX_90 = volSPX_90.resample('Q').last()

volIBOV_90 = pd.DataFrame(data=df['IBOV Index'])
volIBOV_90 = volIBOV_90.droplevel('FIELD')
volIBOV_90 = volIBOV_90.resample('Q').last()

volbonds_90 = pd.DataFrame(data=df['USGG10YR Index'])
volbonds_90 = volbonds_90.droplevel('FIELD')
volbonds_90 = volbonds_90.resample('Q').last()

voltitul_90 = pd.DataFrame(data=df['GEBR10Y Index'])
voltitul_90 = voltitul_90.droplevel('FIELD')
voltitul_90 = voltitul_90.resample('Q').last()

#Plot series
#ax = plt.gca()
#volSPX_90.plot(kind='line', color='blue', ax=ax)
#volIBOV_90.plot(kind='line', color='green', ax=ax)
#volbonds_90.plot(kind='line', color='red', ax=ax)
#voltitul_90.plot(kind='line', color='yellow', ax=ax)
#plt.show()

# Normalized series SPX and US Bonds
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

# Info
volUS.info()
volBR.info()

# Plotting normalized
ax = plt.gca()
volUS.plot(kind='line', y='SPX Index Normalized', color='blue', ax=ax)
volBR.plot(kind='line', y='IBOV Index Normalized', color='green', ax=ax)
volUS.plot(kind='line', y='Bonds Vol. Normalized', color='red', ax=ax)
volBR.plot(kind='line', y='Titulos Vol. Normalized', color='yellow', ax=ax)
plt.show()

# Average Volatility
volBR["Avg Vol US"] = volUS.mean(numeric_only = True, axis=1)
volUS["Avg Vol BR"] = volBR.mean(numeric_only = True, axis=1)
