from shape_data import Midpoint # Need the Midpoint class from the shape_data db in order to access r-squared values
import pandas as pd
import numpy as np

nysedata = pd.read_csv('./company_data/nyse_companies.csv') # Reads in company files since tickers should be unique
nasdaqdata = pd.read_csv('./company_data/nasdaq_companies.csv')
tickers = list(nysedata['Symbol'].unique()) # Extracts the unique list of tickers from nyse files
tickers.extend(list(nasdaqdata['Symbol'].unique())) # Extracts the unique list of tickers from nasdaq files
tickers = list(set(tickers)) # Creates a set of tickers, which prevents duplicate values


# Iteratively creates a dictionary for all tickers, where tickers are the keys and the values are arrays
#ticker_stats = {tick:[] for tick in tickers}
# Creates a list in which the tickers with null r-squared values will be stored
#null_rsqrd = []
ticker_stats = {tick:[] for tick in tickers}
null_rsqrd = []

'''
The "rsqrd" function populates the value arrays for each ticker key in the 'ticker_stats' dictionary
For each ticker key, the value arrays will be populated in the following manner:
    {'ticker': [rsqrd mean of lead time 60, std of lead time 60, mean 300, std 300, mean 600, std 600]}
'''
def rsqrd():
    for tick in tickers:# Function will loop through each ticker
        for ll in [0.05,60,600]: # List of lead times through which to iterate for each ticker
            # Empty array where r-squared values will temporarily be stored specific to a ticker/lead-time pair
            temp_rsqrd = []
            '''
            The subsequent loop selects all db rows matching a specific ticker and lead
            For each loop, the number of rows selected should be equal to the number of months of data
            In this case, we have 1 yr of data, so 12 rows should be selected for each ticker and lead time
            '''
            for ii in Midpoint.select().where((Midpoint.ticker == tick) & (Midpoint.lead == ll)):
                if pd.isnull(ii.r_squared): # Stores the ticker/lead pairs with null rsqrd values in 'null_rsqrd' array
                    null_rsqrd.extend([tick,ll,ii.month])
                else: # If rsqrd values aren't null, they are appended to the temp_rsqrd array
                    temp_rsqrd.append(ii.r_squared)
            #For each ticker/lead pair, the mean and std are calculated and appended to the value array specific to the ticker key
            if len(temp_rsqrd) > 0:
                ticker_stats[tick].extend([np.mean(temp_rsqrd), np.std(temp_rsqrd)])
    return ticker_stats
