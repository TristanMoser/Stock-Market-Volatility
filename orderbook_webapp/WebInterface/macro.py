import pandas as pd
import numpy as np
from gc_data import Asset
from shape_data import Midpoint
import peewee

nysedata = pd.read_csv('./company_data/nyse_companies.csv') # Reads in company files since tickers should be unique
nasdaqdata = pd.read_csv('./company_data/nasdaq_companies.csv')
tickers = list(nysedata['Symbol'].unique()) # Extracts the unique list of tickers from nyse files
tickers.extend(list(nasdaqdata['Symbol'].unique())) # Extracts the unique list of tickers from nasdaq files
tickers = list(set(tickers)) # Creates a set of tickers, which prevents duplicate values

macro_stats = {tick:[] for tick in tickers}

def macro(lead_time,Exchange):
    for tick in tickers:
        temp = []
        for ii in Asset.select().where((Asset.ticker == tick) & (Asset.lead == lead_time) & (Asset.exchange == Exchange)):
            temp_beta = np.abs(ii.beta1)
            try:
                causers = Midpoint.select().where((Midpoint.ticker == ii.causer) & (Midpoint.lead == lead_time)).get()
                temp_rsqrd = causers.r_squared
                if temp_rsqrd is None:
                    temp_rsqrd = 0
            except peewee.DoesNotExist:
                temp_rsqrd = 0
            temp.append((temp_beta)*(temp_rsqrd))
        macro_stats[tick] = np.mean(temp)
    return macro_stats
