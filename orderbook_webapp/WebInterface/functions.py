import pandas as pd
import numpy as np
from gc_data import Asset
from shape_data import Midpoint
import peewee

#Create a comprehensive list of all tickers in both exhanges
nysedata = pd.read_csv('./company_data/nyse_companies.csv') # Reads in company files since tickers should be unique
nasdaqdata = pd.read_csv('./company_data/nasdaq_companies.csv')
tickers = list(nysedata['Symbol'].unique()) # Extracts the unique list of tickers from nyse files
tickers.extend(list(nasdaqdata['Symbol'].unique())) # Extracts the unique list of tickers from nasdaq files
tickers = list(set(tickers)) # Creates a set of tickers, which prevents duplicate values


def rsqrd():
    '''
    The "rsqrd" function populates the values for each ticker key in the 'ticker_stats' dictionary.

    The average rsqrd value is calculated for each lead time across all months that the ticker appears
    in the data.

    Returns:
    ticker_stats - dictionary
                  The final dictionary is populated in the following format:
                  {'ticker': [mean 60, std 60, mean 300, std 300, mean 600, std 600]}
                  Note: each number represents the associated lead time
    '''
    ticker_stats = {tick:[] for tick in tickers}
    null_rsqrd = []
    for tick in tickers:# Function will loop through each ticker
        for ll in [0.05,60,600]: # List of lead times through which to iterate for each ticker
            # Empty array where r-squared values will temporarily be stored specific to a ticker/lead-time pair
            temp_rsqrd = []
            '''
            The subsequent loop selects all db rows matching a specific ticker and lead
            For each loop, the number of rows selected should be equal to the number of months of data
            In this case, we have 1 yr of data, so 12 rows should be selected for each ticker and lead time.
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


def manip(lead_time,Exchange,month):
    '''
    The "manip" function populates the values for each ticker key in the 'manip_stats' dictionary.

    For each ticker's causer, the neighbor manipulability score is calculated by taking the absolute
    value of the ticker's first beta coefficient and multiplying that value by the causer's rsqrd value.
    The average is then taken across the five major causers.

    Parameters:
    lead_time - int
                The time horizon used for the estimation
    Exchange  - string
                Either 'NASDAQ' or 'NYSE'
    month     - int
                The number corresponding to month, e.g. 4 for April

    Returns:
    manip_stats - dictionary
                  The final dictionary is populated in the following format:
                  {'ticker': [rsqrd value, average neighbor manipulablility score]}
    '''
    manip_stats = {tick:[] for tick in tickers}
    for tick in tickers:
        temp = []
        try:
            rsquared = Midpoint.select().where((Midpoint.ticker == tick) &
                                               (Midpoint.month == month) &
                                               (Midpoint.lead == lead_time)).get().r_squared
        except peewee.DoesNotExist:
            rsquared = np.nan

        #Loop through all entries in the Asset class for ticker in exchange with specified lead time
        for ii in Asset.select().where((Asset.ticker == tick) & (Asset.lead == lead_time) & (Asset.exchange == Exchange)):
            temp_beta = np.abs(ii.beta1) #Store absolute value of beta for each causer
            try:
                #Select row in Midpoint class corresonding to the ticker's causer
                causers = Midpoint.select().where((Midpoint.ticker == ii.causer) &
                                                  (Midpoint.lead == lead_time) &
                                                  (Midpoint.month == month)).get().r_squared
                ###temp_rsqrd = causers.r_squared #Store causer's rqrd value
                if causers is None: #Eliminate NoneTypes
                    causers = np.nan
            except peewee.DoesNotExist:#Account for causers not in database
                causers = np.nan
            if np.isnan((temp_beta*causers)) == False:
                temp.append((temp_beta)*(causers)) #Create manipulability score and store in dictionary
        manip_stats[tick] = [rsquared, np.mean(temp)]
    return manip_stats
