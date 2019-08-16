from bloomberg import BBG
import pandas as pd

from bloomberg import BBG
import pandas as pd

start_date = '30-mar-2015'
end_date = pd.to_datetime('today')

field = ['BEST_ESTIMATE_FCF', 'BEST_SALES', 'BEST_EBIT', 'BEST_EPS_GAAP', 'BEST_NET_GAAP', 'BEST_TARGET_PRICE', 'BEST_ANALYST_RATING']

bbg = BBG()

# Grabs tickers and fields

for i in field:
### "BEST_CURRENT_PROFIT" e "YLD_ANNUAL_MID" deram erro

    df = bbg.fetch_series(securities= ['ABEV3 BZ Equity', 'AZUL4 BZ Equity', 'B3SA3 BZ Equity', 'BBAS3 BZ Equity', 'BBDC3 BZ Equity', 'BBDC4 BZ Equity', 'BBSE3 BZ Equity', 'BRAP4 BZ Equity', 'BRDT3 BZ Equity', 'BRFS3 BZ Equity', 'BRKM5 BZ Equity', 'BRML3 BZ Equity', 'BTOW3 BZ Equity', 'CCRO3 BZ Equity', 'CIEL3 BZ Equity', 'CMIG4 BZ Equity', 'CSAN3 BZ Equity', 'CSNA3 BZ Equity', 'CVCB3 BZ Equity', 'CYRE3 BZ Equity', 'ECOR3 BZ Equity', 'EGIE3 BZ Equity', 'ELET3 BZ Equity', 'ELET6 BZ Equity', 'EMBR3 BZ Equity', 'ENBR3 BZ Equity', 'EQTL3 BZ Equity', 'FLRY3 BZ Equity', 'GGBR4 BZ Equity', 'GOAU4 BZ Equity', 'GOLL4 BZ Equity', 'HYPE3 BZ Equity', 'IGTA3 BZ Equity', 'IRBR3 BZ Equity', 'ITSA4 BZ Equity', 'ITUB4 BZ Equity', 'JBSS3 BZ Equity', 'KLBN11 BZ Equity', 'KROT3 BZ Equity', 'LAME4 BZ Equity', 'LREN3 BZ Equity', 'MGLU3 BZ Equity', 'MRFG3 BZ Equity', 'MRVE3 BZ Equity', 'MULT3 BZ Equity', 'NATU3 BZ Equity', 'PCAR4 BZ Equity', 'PETR3 BZ Equity', 'PETR4 BZ Equity', 'QUAL3 BZ Equity', 'RADL3 BZ Equity', 'RAIL3 BZ Equity', 'RENT3 BZ Equity', 'SANB11 BZ Equity', 'SBSP3 BZ Equity', 'SMLS3 BZ Equity', 'SUZB3 BZ Equity', 'TAEE11 BZ Equity', 'TIMP3 BZ Equity', 'UGPA3 BZ Equity', 'USIM5 BZ Equity', 'VALE3 BZ Equity', 'VIVT4 BZ Equity', 'VVAR3 BZ Equity', 'WEGE3 BZ Equity', 'YDUQ3 BZ Equity'],
                      fields=[i],
                      startdate=start_date,
                      enddate=end_date)

    print(df)
