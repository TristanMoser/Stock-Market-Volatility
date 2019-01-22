# uncompyle6 version 2.14.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 20 2017, 18:23:56)
# [GCC 5.4.0 20160609]
# Embedded file name: /Users/ssc7/SkyDrive/Documents/DHS/WebInterface/shape_data.py
# Compiled at: 2016-12-12 16:20:19
import os, pandas as pd
from peewee import *
from pprint import pprint
db = SqliteDatabase('shape_data.db')
#db.connect()

class BaseModel(Model):

    class Meta:
        """
        The 'BaseModel' class is defined here and will serve as the parent class,
        inheriting attributes from the Peewee object, 'Model'.

        Defining the 'Meta' class within the BaseModel parent class establishes the
        database connection for all child classes.

        Creating a BaseModel establishes a DB connection and
        circumvents the need to specify a DB connection for
        subsequent models. For example, the 'Midpoint' class
        created below automatically inherits the DB connection
        from 'BaseModel'.
        """
        database = db


class Midpoint(BaseModel):
    """
    This defines the 'Midpoint' class used to structure the database table.

    Midpoint represents the midpoint prices given bids and asks specific to a single ticker.
    The rsqrd value from the regression is also provided here.
    """
    ticker = CharField()
    month = CharField()
    lead = FloatField()
    constant = FloatField(null=True)
    execution = FloatField(null=True)
    outer_adds = FloatField(null=True)
    adds = FloatField(null=True)
    bids_001 = FloatField(null=True)
    asks_001 = FloatField(null=True)
    bids_005 = FloatField(null=True)
    asks_005 = FloatField(null=True)
    bids_01 = FloatField(null=True)
    asks_01 = FloatField(null=True)
    bids_02 = FloatField(null=True)
    asks_02 = FloatField(null=True)
    bids_05 = FloatField(null=True)
    asks_05 = FloatField(null=True)
    bids_10 = FloatField(null=True)
    asks_10 = FloatField(null=True)
    bids_15 = FloatField(null=True)
    asks_15 = FloatField(null=True)
    bids_30 = FloatField(null=True)
    asks_30 = FloatField(null=True)
    se_constant = FloatField(null=True)
    se_execution = FloatField(null=True)
    se_outer_adds = FloatField(null=True)
    se_adds = FloatField(null=True)
    se_bids_001 = FloatField(null=True)
    se_asks_001 = FloatField(null=True)
    se_bids_005 = FloatField(null=True)
    se_asks_005 = FloatField(null=True)
    se_bids_01 = FloatField(null=True)
    se_asks_01 = FloatField(null=True)
    se_bids_02 = FloatField(null=True)
    se_asks_02 = FloatField(null=True)
    se_bids_05 = FloatField(null=True)
    se_asks_05 = FloatField(null=True)
    se_bids_10 = FloatField(null=True)
    se_asks_10 = FloatField(null=True)
    se_bids_15 = FloatField(null=True)
    se_asks_15 = FloatField(null=True)
    se_bids_30 = FloatField(null=True)
    se_asks_30 = FloatField(null=True)
    rse_constant = FloatField(null=True)
    rse_execution = FloatField(null=True)
    rse_outer_adds = FloatField(null=True)
    rse_adds = FloatField(null=True)
    rse_bids_001 = FloatField(null=True)
    rse_asks_001 = FloatField(null=True)
    rse_bids_005 = FloatField(null=True)
    rse_asks_005 = FloatField(null=True)
    rse_bids_01 = FloatField(null=True)
    rse_asks_01 = FloatField(null=True)
    rse_bids_02 = FloatField(null=True)
    rse_asks_02 = FloatField(null=True)
    rse_bids_05 = FloatField(null=True)
    rse_asks_05 = FloatField(null=True)
    rse_bids_10 = FloatField(null=True)
    rse_asks_10 = FloatField(null=True)
    rse_bids_15 = FloatField(null=True)
    rse_asks_15 = FloatField(null=True)
    rse_bids_30 = FloatField(null=True)
    rse_asks_30 = FloatField(null=True)
    r_squared = FloatField(null=True)
    num_messages = FloatField(null=True)
    num_days = FloatField(null=True)
    #null=True permits nulls in the field

class Volatility(BaseModel):
    """
    This defines the 'Volatility' class used to structure the database table.

    Volatility represents the measure of midpoint price variation given bids
    and asks specific to a single ticker as well as the rsqrd value.
    """
    ticker = CharField()
    month = CharField()
    lead = FloatField()
    constant = FloatField(null=True)
    execution = FloatField(null=True)
    outer_adds = FloatField(null=True)
    adds = FloatField(null=True)
    bids_001 = FloatField(null=True)
    asks_001 = FloatField(null=True)
    bids_005 = FloatField(null=True)
    asks_005 = FloatField(null=True)
    bids_01 = FloatField(null=True)
    asks_01 = FloatField(null=True)
    bids_02 = FloatField(null=True)
    asks_02 = FloatField(null=True)
    bids_05 = FloatField(null=True)
    asks_05 = FloatField(null=True)
    bids_10 = FloatField(null=True)
    asks_10 = FloatField(null=True)
    bids_15 = FloatField(null=True)
    asks_15 = FloatField(null=True)
    bids_30 = FloatField(null=True)
    asks_30 = FloatField(null=True)
    se_constant = FloatField(null=True)
    se_execution = FloatField(null=True)
    se_outer_adds = FloatField(null=True)
    se_adds = FloatField(null=True)
    se_bids_001 = FloatField(null=True)
    se_asks_001 = FloatField(null=True)
    se_bids_005 = FloatField(null=True)
    se_asks_005 = FloatField(null=True)
    se_bids_01 = FloatField(null=True)
    se_asks_01 = FloatField(null=True)
    se_bids_02 = FloatField(null=True)
    se_asks_02 = FloatField(null=True)
    se_bids_05 = FloatField(null=True)
    se_asks_05 = FloatField(null=True)
    se_bids_10 = FloatField(null=True)
    se_asks_10 = FloatField(null=True)
    se_bids_15 = FloatField(null=True)
    se_asks_15 = FloatField(null=True)
    se_bids_30 = FloatField(null=True)
    se_asks_30 = FloatField(null=True)
    rse_constant = FloatField(null=True)
    rse_execution = FloatField(null=True)
    rse_outer_adds = FloatField(null=True)
    rse_adds = FloatField(null=True)
    rse_bids_001 = FloatField(null=True)
    rse_asks_001 = FloatField(null=True)
    rse_bids_005 = FloatField(null=True)
    rse_asks_005 = FloatField(null=True)
    rse_bids_01 = FloatField(null=True)
    rse_asks_01 = FloatField(null=True)
    rse_bids_02 = FloatField(null=True)
    rse_asks_02 = FloatField(null=True)
    rse_bids_05 = FloatField(null=True)
    rse_asks_05 = FloatField(null=True)
    rse_bids_10 = FloatField(null=True)
    rse_asks_10 = FloatField(null=True)
    rse_bids_15 = FloatField(null=True)
    rse_asks_15 = FloatField(null=True)
    rse_bids_30 = FloatField(null=True)
    rse_asks_30 = FloatField(null=True)
    r_squared = FloatField(null=True)
    num_messages = FloatField(null=True)
    num_days = FloatField(null=True)

var_names = [
 'ticker', 'constant', 'execution', 'outer_adds', 'adds', 'bids_001', 'asks_001', 'bids_005',
 'asks_005', 'bids_01', 'asks_01', 'bids_02', 'asks_02', 'bids_05', 'asks_05', 'bids_10', 'asks_10',
 'bids_15', 'asks_15', 'bids_30', 'asks_30', 'se_constant', 'se_execution', 'se_outer_adds',
 'se_adds', 'se_bids_001', 'se_asks_001', 'se_bids_005', 'se_asks_005', 'se_bids_01', 'se_asks_01',
 'se_bids_02', 'se_asks_02', 'se_bids_05', 'se_asks_05', 'se_bids_10', 'se_asks_10', 'se_bids_15',
 'se_asks_15', 'se_bids_30', 'se_asks_30', 'rse_constant', 'rse_execution', 'rse_outer_adds', 'rse_adds',
 'rse_bids_001', 'rse_asks_001', 'rse_bids_005', 'rse_asks_005', 'rse_bids_01', 'rse_asks_01',
 'rse_bids_02', 'rse_asks_02', 'rse_bids_05', 'rse_asks_05', 'rse_bids_10', 'rse_asks_10', 'rse_bids_15',
 'rse_asks_15', 'rse_bids_30', 'rse_asks_30', 'r_squared', 'num_messages', 'num_days']

def create_tables():
    """
    The 'create_tables' function will creat the 'Volatility' and 'Midpoint' tables
    in the database in order to read in data.

    This function will try to delete the tables if they already exist. If they do
    not yet exist, then this function will create the tables and connect them to
    the database.
    """
    try:
        Volatility.delete()
        Midpoint.delete()
    except Exception as e:
        print(e)
        print("Couldn't delete tables (is the .db file there?)")
        pass

    try:
        db.create_tables([Volatility, Midpoint])
    #db.connect()
    except Exception as e:
        print(e)
        print("Stuff couldn't be created")

if __name__ == '__main__': #execute only if run as a script; main function
    create_tables()
    files = [ f for f in os.listdir('./shape_data/') if os.path.isfile('./shape_data/' + f) ]
    #Above creates a list, 'files', from true files in the directory
    new_lead = {'0.05': 0.05, '60.0': 60, '300.0': 600}
    for ff in files: #loops through each file, 'ff', in 'file' array
        parts = ff.split('_') #stores pieces of file name in 'parts' object split at '_'
        if len(parts) > 1:
            if parts[1] == 'vol': #'vol' = volatility
                month = parts[0][0:3] #extracts the month from the file name
                if 'nodiff' not in parts:
                    lead = parts[-1].split('.csv')[0] #lead is time interval in seconds that data is collected
                    dep_var = 'vol' #dependent variable = volatility
                    the_file = pd.read_csv('./shape_data/' + ff, skiprows=1, names=var_names)
                    ddict = the_file.to_dict(orient='index')#{'index':{'col': value,...}}
                    for ii, dd in ddict.items():#returns (key, value) tuples...i.e. (ii,dd)
                        dd['month'] = month
                        dd['lead'] = new_lead[lead]
                        vv = Volatility(**dd)# creates new row in DB from ordered tuple
                        vv.save() # '**dd' takes dictionary format and transforms it to [key1=value1 key2=value2...]
                        			# because 'Volatility' requires args in specific format, key = 'value' whereas dictionary uses ':'

            if parts[1] == 'lead':
                month = parts[0][0:3]
                if 'nodiff' not in parts:
                    lead = parts[-1].split('.csv')[0]
                    dep_var = 'vol'
                    the_file = pd.read_csv('./shape_data/' + ff, skiprows=1, names=var_names)
                    ddict = the_file.to_dict(orient='index')
                    #pprint(ddict)
                    for ii, dd in ddict.items():
                        dd['month'] = month
                        dd['lead'] = new_lead[lead]
                        mm = Midpoint(**dd)
                        mm.save()
# okay decompiling shape_data.pyc
