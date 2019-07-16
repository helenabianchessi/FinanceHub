import pandas as pd

from dataapi import FRED

import datetime

from datetime import date

getdata = FRED()

#fetching GDP
df_gr = pd.DataFrame(getdata.fetch("GDPC1"))
df_gr = df_gr['GDPC1'].resample('Q').mean()
df_gr = df_gr.pct_change(4)
#print(df_gr)

#fetching potential GDP until today's date
today = date.today()
df_expectedgr = pd.DataFrame(getdata.fetch("GDPPOT", None, today))
df_expectedgr = df_expectedgr['GDPPOT'].resample('Q').mean()
df_expectedgr = df_expectedgr.pct_change(4)

#fetching CFNAI
df_CFNAI = pd.DataFrame(getdata.fetch("CFNAI"))
df_CFNAI = df_CFNAI.resample('Q').mean()
#print(df_CFNAI)

#fetching real earnings
df_realear = getdata.fetch("LES1252881600Q")
df_realear = df_realear['LES1252881600Q'].resample("Q").mean()
df_realear = df_realear.pct_change(4)

#Merging DataFrames#

df_realgr = pd.merge(df_expectedgr,df_gr, on='Date', how='outer')

df_realgr = pd.merge(df_realgr,df_realear, on='Date', how='outer')

df_realgr = pd.merge(df_realgr,df_CFNAI, on='Date', how='outer')

print(df_realgr)

#adding a column with average

#df_realgr["average"] = ((df_realgr["GDPC1"] + df_realgr["GDPPOT"] + df_realgr["LES1252881600Q"] + df_realgr["CFNAI"])/6)
