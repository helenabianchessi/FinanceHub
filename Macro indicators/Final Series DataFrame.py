import pandas as pd

df_growth = df_realgr["Real Growth"]
df_vol = AvgVolUS['Avg Vol US']
df_series = df_inf["inflation"]

df_series = pd.merge(df_series, df_growth, on="Date", how="outer")
df_series = pd.merge(df_series, df_vol, on="Date", how="outer")
from scipy.stats import zscore

numeric_cols = df_series.select_dtypes(include=[np.number]).columns
df[numeric_cols].apply(zscore)

print(df_series)