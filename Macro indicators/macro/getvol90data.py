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

# Pulling IBOVESPA and S&P indexes volatility
#   Original Date: '28-fev-1967'

start_date = pd.to_datetime('01-jan-2010')
end_date = pd.to_datetime('today')

df = bbg.fetch_series(securities=['SPX Index', 'IBOV Index'],
                      fields=['VOLATILITY_90D'],
                      startdate=start_date,
                      enddate=end_date)

volSPX_90 = pd.DataFrame(data=df['SPX Index'])
volSPX_90 = volSPX_90.droplevel('FIELD')
volSPX_90 = volSPX_90.resample('Q').last()

volIBOV_90 = pd.DataFrame(data=df['IBOV Index'])
volIBOV_90 = volIBOV_90.droplevel('FIELD')
volIBOV_90 = volIBOV_90.resample('Q').last()

#ax = plt.gca()

#volSPX_90.plot(kind='line', color='blue', ax=ax)
#volIBOV_90.plot(kind='line', color='green', ax=ax)

#plt.show()

# Normalized series SPX

x = np.array(volSPX_90['SPX Index'])
x = x.reshape(-1,1)
spxnorm = min_max_scaler.fit_transform(x)

volnormSPX = volSPX_90
volnormSPX['SPX Index Normalized'] = ''
volnormSPX['SPX Index Normalized'] = spxnorm
volnormSPX = volnormSPX.drop('SPX Index', axis=1)

# Normalized series IBOV

y = np.array(volIBOV_90['IBOV Index'])
y = y.reshape(-1,1)
ibovnorm = min_max_scaler.fit_transform(y)

volnormIBOV = volIBOV_90
volnormIBOV['IBOV Index Normalized'] = ''
volnormIBOV['IBOV Index Normalized'] = ibovnorm
volnormIBOV = volnormIBOV.drop('IBOV Index', axis=1)

# Info

volnormSPX.info()
volnormIBOV.info()

# Plotting

ax = plt.gca()

volnormSPX.plot(kind='line', y='SPX Index Normalized', color='blue', ax=ax)
volnormIBOV.plot(kind='line', y='IBOV Index Normalized', color='green', ax=ax)

plt.show()
