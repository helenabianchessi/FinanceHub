import pandas as pd
from dataapi import FRED
import datetime
from datetime import date
from sklearn import preprocessing
import numpy as np

getdata = FRED()

#fetching CPI
df_cpi = pd.DataFrame(getdata.fetch("CPIAUCSL"))
df_cpi = df_cpi['CPIAUCSL'].resample('Q').mean()

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
df_gdpdef = pd.DataFrame(getdata.fetch("GDPDEF"))
df_gdpdef = df_gdpdef['GDPDEF'].resample('Q').mean()
df_gdpdef = df_gdpdef.pct_change(4)
df_gdpdef = df_gdpdef.dropna()

#normalizing GDP deflator
d = df_gdpdef.values
d = d.reshape(-1, 1)
d_scaled = min_max_scaler.fit_transform(d)
df_gdpdef_norm = pd.DataFrame(d_scaled, index=df_gdpdef.index, columns=['GDP Deflator Normalized'])