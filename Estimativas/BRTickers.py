import pandas as pd
import numpy as np
import blpapi
from bloomberg import BBG

start_date = '30-mar-2015'
end_date = pd.to_datetime('today')
bbg = BBG()

#fetching Bloomberg Estimates BEst (Bloomberg Estimates)
df = bbg.fetch_series(securities=['PETR4', 'MGLU3'],
                      fields=['BE008', 'BE001'],
                      startdate=start_date,
                      enddate=end_date)

PetroMgluEst = pd.DataFrame(data=df)
print(PetroMgluEst)