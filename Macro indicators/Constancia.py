import pandas as pd
from dataapi import FRED
import datetime
from datetime import date
from sklearn import preprocessing
import numpy as np

getdata = FRED()

#fetching GDP
df_gr = pd.DataFrame(getdata.fetch("GDPC1"))
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
today = date.today()
df_expectedgr = pd.DataFrame(getdata.fetch("GDPPOT", None, today))
df_expectedgr = df_expectedgr['GDPPOT'].resample('Q').mean()
df_expectedgr = df_expectedgr.pct_change(4)
df_expectedgr = df_expectedgr.dropna()

#normalizing potential GDP
y = df_expectedgr.values
y = y.reshape(-1,1)
y_scaled = min_max_scaler.fit_transform(y)
df_expectedgr_norm = pd.DataFrame(y_scaled, index=df_expectedgr.index, columns=['POTGDP Normalized'])

#fetching CFNAI
df_CFNAI = pd.DataFrame(getdata.fetch("CFNAI"))
df_CFNAI = df_CFNAI.resample('Q').mean()
df_CFNAI = df_CFNAI.dropna()

#normalizing CFNAI
w = df_CFNAI.values
w = w.reshape(-1,1)
w_scaled = min_max_scaler.fit_transform(w)
df_CFNAI_norm = pd.DataFrame(w_scaled, index=df_CFNAI.index, columns=['CFNAI Normalized'])

#fetching real earnings
df_realear = getdata.fetch("LES1252881600Q")
df_realear = df_realear['LES1252881600Q'].resample("Q").mean()
df_realear = df_realear.pct_change(4)
df_realear = df_realear.dropna()

#normalizing real earnings
a = df_realear.values
a = a.reshape(-1,1)
a_scaled = min_max_scaler.fit_transform(a)
df_realear_norm = pd.DataFrame(a_scaled, index=df_realear.index, columns=['Real Earnings Normalized'])

#Merging DataFrames#

df_realgr = pd.merge(df_expectedgr_norm,df_gr_norm, on='Date', how='outer')

df_realgr = pd.merge(df_realgr,df_realear_norm, on='Date', how='outer')

df_realgr = pd.merge(df_realgr,df_CFNAI_norm, on='Date', how='outer')

#adding a column with average

df_realgr["Real Growth"] = df_realgr.mean(numeric_only = True, axis=1)

print(df_realgr)