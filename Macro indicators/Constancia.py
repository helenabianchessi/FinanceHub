import pandas as pd

from dataapi import FRED

import datetime

getdata = FRED()

#fetching GDP, Pontential GDP and CFNAI from FRED #
df_gr = pd.DataFrame(getdata.fetch("GDPC1"))
#df_gr = df_gr.pct_change(4)

df_expectedgr = pd.DataFrame(getdata.fetch("GDPPOT"))
df_expectedgr = df_expectedgr.pct_change(4)

df_CFNAI = pd.DataFrame(getdata.fetch("CFNAI"))
df_CFNAI = df_CFNAI.resample('Q')
print(df_CFNAI)

#fetching real earnings from FRED#
df_realear = getdata.fetch("LES1252881600Q")
df_realear = df_realear.pct_change(4)

#Merging DataFrames#

df_realgr = pd.merge(df_expectedgr,df_gr, on='Date', how='outer')

df_realgr = pd.merge(df_realgr,df_realear, on='Date', how='outer')

#df_realgr = pd.merge(df_realgr,df_CFNAI, on='Date', how='outer')

#adding a column with average#

#df_realgr["average"] = ((df_realgr["GDPC1"] + df_realgr["GDPPOT"] + df_realgr["LES1252881600Q"] + df_realgr["CFNAI"])/6)
