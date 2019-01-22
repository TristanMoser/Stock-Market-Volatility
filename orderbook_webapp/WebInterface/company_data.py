import os
import pandas as pd
import numpy as np
from peewee import *
from functions import rsqrd, manip
import peewee


db = SqliteDatabase('./company_data.db')
db.connect()

class BaseModel(Model):
    """
    This defines the Base Model which specifies the database subsequent classes will use.

    The class inherits its attributes from the standard Peewee Model.
    Meta is a class from the Peewee Model that allows a database to be set.
    """
    class Meta:
        database = db


class Company(BaseModel):
    """
    This is the structure for which a table in the database will be made to
    represent all the meta data for each company.

    The table contains fields for the ticker handle, its company name,
    the year of its first Initial Public Offering, the sector and Industry
    the company belongs to, both averages and standard deviations for each
    lead time, and average neighbor manipulability scores.

    Each of the corresponding fields listed will be columns for the created table.
    """
    ticker = CharField()
    Name = CharField()
    IPOYear = CharField()
    Sector = CharField()
    Industry = CharField()
    r2mean10 = FloatField(null=True)
    r2std10 = FloatField(null=True)
    r2mean60 = FloatField(null=True)
    r2std60 = FloatField(null=True)
    r2mean600 = FloatField(null=True)
    r2std600 = FloatField(null=True)
    avg_neighbor_manip_score = FloatField(null=True)
    rsqrd_neighbor_plot = FloatField(null=True)
    #null=True permits nulls in the field


def create_tables():
    """
    This function will create a table in the database so that data can be read into it.

    First, it will delete the Company table if that table has already been created.
    Next, it will create a table in the database using the information from the
    Company class previously defined.
    """
    try:
        Company.delete()
    except:
        pass
    try:
        db.create_tables([Company])
        #db.connect()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    #This will only run if this file is the original file being run and will not if the file is being exported somewhere else.
    create_tables()
    # Create the database with all of the files that are present in the /company_data/ directory
    data_dir = os.path.join(os.getcwd(), "company_data/")
    ticker_stats = rsqrd()#The rsqrd function will create a dictionary of rsqrd stats. See rsqrd.py for more info
    manip_stats = manip(60,'NASDAQ','JAN')#Calculate average neighbor scores with rsqrds
    #Note: we only take one combination for prototype
    files = [ f for f in os.listdir(data_dir) ]#This creates a list of all the files in the directory
    #print(files)
    for ff in files:
        suffix = ff.split(".")[1]#This split will help distinguish the file types i.e.('.csv','.pdf')
        #print(suffix)
        if suffix == "csv":
            the_path = os.path.join(data_dir, ff)
            the_file = pd.read_csv(the_path)
            #Match column names with names in Company Class
            the_file.rename(columns={"Symbol": "ticker", "industry": "Industry", "IPOyear": "IPOYear"}, inplace=True)
            #Convert dataframe to a dictionary of dictionaries where each key represents a company_data
            #Each company contains a dictionary corresponding to the columns in the dataframe
            ddict = the_file.to_dict(orient="index")
            #loop over each key (company),value(column) to poplulate each company as a table entry
            for ii, dd in ddict.items():
                # Delete the columns I don't need.
                del dd['LastSale']
                del dd['MarketCap']
                del dd['Summary Quote']
                #Select rsqrd stats for the specific company
                try:
                    r2stats = ticker_stats[dd['ticker']]
                #If the company is not in the rsqrd list, then it will create a blank list. This prevents an empty entry in the database
                except KeyError:
                    r2stats = []
                #To avoid an IndexError, condition on len(r2stats) and then take the appropriate entry from r2stats
                if len(r2stats) >0:
                    dd['r2mean10'] = r2stats[0]
                    dd['r2std10'] = r2stats[1]
                    dd['r2mean60'] = r2stats[2]
                    dd['r2std60'] = r2stats[3]
                    dd['r2mean600'] = r2stats[4]
                    dd['r2std600'] = r2stats[5]
                #Create null entries for companies with empty r2stats lists
                else:
                    dd['r2mean10'] = np.nan
                    dd['r2std10'] = np.nan
                    dd['r2mean60'] = np.nan
                    dd['r2std60'] = np.nan
                    dd['r2mean600'] = np.nan
                    dd['r2std600'] = np.nan
                try:
                    macrostats = manip_stats[dd['ticker']]
                except KeyError:
                    macrostats = []
                if len(macrostats)>0:
                    dd['avg_neighbor_manip_score'] = macrostats[1]
                    dd['rsqrd_neighbor_plot'] = macrostats[0]
                else:
                    dd['avg_neighbor_manip_score'] = np.nan
                    dd['rsqrd_neighbor_plot'] = np.nan
                #Create and save row to the Company database
                cc = Company(**dd)
                cc.save()
