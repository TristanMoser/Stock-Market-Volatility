import os
import pandas as pd
from peewee import *

db = SqliteDatabase("gc_data.db")
db.connect()

class BaseModel(Model):
    """
	This defines the Base Model which specifies the database subsequent classes will use.

    The class inherits its attributes from the standard Peewee Model.
    Meta is a class from the Peewee Model that allows a database to be set.
    """
    class Meta:
        database = db

class Asset(BaseModel):
    """
    This is the structure for which a table in the database will be made to
    represent an individual asset's Granger Causality test results.

    The table contains fields for the ticker handle, which exchange it is in,
    the candidate for Granger causality, the lead time horizon, and the
    statistical significance/coefficient estimates for the Granger Causality
    tests, for each model with lags ranging from 1 to 5 inclusive.

    Each of the corresponding fields listed will be columns for the created table.
    """
    ticker = CharField()
    exchange = CharField()
    causer = CharField()
    month = CharField()
    lead = IntegerField()
    lag1 = FloatField()
    lag2 = FloatField()
    lag3 = FloatField()
    lag4 = FloatField()
    lag5 = FloatField()
    beta1 = FloatField()
    beta2 = FloatField()
    beta3 = FloatField()
    beta4 = FloatField()
    beta5 = FloatField()
    rank = IntegerField()

def create_tables():
    """
    This function will create a table in the database so that data can be read into it.

    First, it will delete the Asset table if that table has already been created.
    Next, it will create a table in the database using the information from the
    Asset class previously defined.
    """
    try:
        Asset.delete()
    except:
        pass
    try:
        db.create_tables([Asset])
        #db.connect()
    except Exception as e:
        print(e)

#The following will only occur if the original file is being run:
#Create the database with all of the files that are present.
if __name__ == "__main__":
    create_tables()
    #All files found within the GC directories are compiled into lists for NYSE and NASDAQ respectively.
    rootNY = '../NYSE/Granger Causality Tests/'
    rootNA = '../NASDAQ/Granger Causality Tests/'
    filesNY = [ rootNY + f for f in os.listdir(rootNY) if os.path.isfile(rootNY + f) ]
    filesNA = [ rootNA + f for f in os.listdir(rootNA) if os.path.isfile(rootNA + f) ]
    #print(filesNY)
    #print(filesNA)

    #First populate database with NYSE results
    for ff in filesNY:
        #print(ff)
        # Parse the documents to get file names by using "/"
        name = ff.split("/")[-1]
        #print(name)
        if name[0:3] == "gc_":        # Only deal with the data files
            # Parse the names using "_" to get duration and month
            name_parts = name.split("_")
            month = name_parts[2]
            #Because the months in the file name are different than what the server expects, we change them
            month_change = {'01':'JAN' , '02': 'FEB', '03': 'MAR', '04':'APR', '05':'MAY', '06':'JUN', '07':'JUL',
			'08': 'AUG', '09':'SEP', '10':'OCT', '11':'NOV', '12':'DEC'}
            new_month = month_change[month]
            lead_time = name_parts[3].split(".")[0]
            # Create pandas dataframe
            the_file = pd.read_csv(ff)
            # Rename columns to match Asset class fields
            the_file.rename(columns={"L1": "lag1", "L2": "lag2", "L3": "lag3", "L4": "lag4", "L5": "lag5", "B1": "beta1", "B2": "beta2", "B3": "beta3", "B4": "beta4", "B5": "beta5"}, inplace=True)

            ddict = the_file.to_dict(orient="index")
            data = list(ddict.values())
            for dd in data:
                dd['month'] = new_month
                dd['lead'] = lead_time
                dd['exchange'] = 'NYSE'

            #print(len(data))
            # The NYSE data is loaded into the database 50 rows at a time to prevent using too much memory
            with db.atomic():
                for idx in range(0, len(data),50):
                    aa = Asset.insert_many(data[idx:idx+50]).execute()

    #populate database with NYSE results. The same steps as above are followed
    for ff in filesNA:
        #print(ff)
        name = ff.split("/")[-1]
        #print(name)
        if name[0:3] == "gc_":        # Only deal with the data files
            # Get duration and month
            name_parts = name.split("_")
            month = name_parts[2]
            month_change = {'01':'JAN' , '02': 'FEB', '03': 'MAR', '04':'APR', '05':'MAY', '06':'JUN', '07':'JUL',
			'08': 'AUG', '09':'SEP', '10':'OCT', '11':'NOV', '12':'DEC'}
            new_month = month_change[month]
            lead_time = name_parts[3].split(".")[0]
            the_file = pd.read_csv(ff)
            the_file.rename(columns={"L1": "lag1", "L2": "lag2", "L3": "lag3", "L4": "lag4", "L5": "lag5", "B1": "beta1", "B2": "beta2", "B3": "beta3", "B4": "beta4", "B5": "beta5"}, inplace=True)

            ddict = the_file.to_dict(orient="index")
            data = list(ddict.values())
            for dd in data:
                dd['month'] = new_month
                dd['lead'] = lead_time
                dd['exchange'] = 'NASDAQ'

            with db.atomic():
                for idx in range(0,len(data),50):
                    aa = Asset.insert_many(data[idx:idx+50]).execute()
