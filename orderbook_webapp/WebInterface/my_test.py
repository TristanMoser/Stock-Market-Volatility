from shape_data import Midpoint
import pandas as pd
import numpy as np

data = pd.read_csv("/Users/tristanmoser/Files/Coding/Condie/orderbook_webapp/Cross-Market/Granger Causality Tests/cross_gc_2016_01_10.csv")
tickers = []
for dd in data.ticker:
    tickers.append(dd)
#ticker = data.ticker.unique()

dbs_60 = []
dbs_300 = []
dbs_600 = []
for tick in tickers:
    test_tick_60 = Midpoint.select().where((Midpoint.ticker == tick) & (Midpoint.lead == 60))
    test_tick_300 = Midpoint.select().where((Midpoint.ticker == tick) & (Midpoint.lead == 300))
    #test_tick_600 = Midpoint.select().where((Midpoint.ticker == tick) & (Midpoint.lead == 600))
    dbs_60.append(test_tick_60)
    dbs_300.append(test_tick_300)
    #dbs_600.append(test_tick_600)

d_60 = {ii:[] for ii in tickers}
d_300 = {ii:[] for ii in tickers}
#d_600 = {ii:[] for ii in tickers}

#Fill dictionary for 60
for number in range(len(tickers)):
    for dd in dbs_60[number]:
        d_60[tickers[number]].append(dd.r_squared)

#Fill dictionary for 300
for number in range(0,2617):
    for dd in dbs_300[number]:
        d_300[tickers[number]].append(dd.r_squared)

#Fill dictionary for 600
#for number in range(0,2617):
#    for dd in dbs_600[number]:
#        d_600[tickers[number]].append(dd.r_squared)
