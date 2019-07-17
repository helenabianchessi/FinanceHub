"""
Authors: Helena Bianchessi and Beatriz Jesus
"""
from bloomberg import BBG
import pandas as pd
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt

bbg = BBG()

# Conference Board Consumer Confidence SA 1985=100
#   Original Date: '28-fev-1967'

start_date = pd.to_datetime('01-jan-2010')
end_date = pd.to_datetime('15-jun-2019')

df = bbg.fetch_series(securities=['CONCCONF Index'],
                      fields=['PX_LAST'],
                      startdate=start_date,
                      enddate=end_date)

concconf = pd.DataFrame(data=df)
concconf = concconf.droplevel(0)
concconf = concconf.reset_index()
concconf = concconf.set_index('TRADE_DATE')
concconf = concconf.resample('Q').mean()

# Normalized series Consumer Confidence

x = np.array(concconf['CONCCONF Index'])
x = x.reshape(-1,1)

min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)

confnorm = concconf
confnorm['CONCCONF Normalized'] = ''
confnorm['CONCCONF Normalized'] = x_scaled
confnorm = confnorm.drop('CONCCONF Index', axis=1)

#confnorm.info()
#print(confnorm)

ax = plt.gca()
confnorm.plot(kind='line', y='CONCCONF Normalized', color='green', ax=ax)
plt.show()