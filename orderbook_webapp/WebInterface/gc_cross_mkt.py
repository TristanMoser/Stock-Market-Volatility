import os
import pandas as pd
from peewee import *

db = SqliteDatabase("gc_cross_mkt.db")
db.connect()

class BaseModel(Model):
	"""
	This defines the Base Model which specifies the database subsequent classes will use.

    The class inherits its attributes from the standard Peewee Model.
    Meta is a class from the Peewee Model that allows a database to be set.
    """
	class Meta:
		database = db

class CrossMkt(BaseModel):
	"""
    This is the structure for which a table in the database will be made to
    represent all the cross market Granger Causality results.

    The table contains fields for the ticker handle, month and lead time,
	indicators for the direction of which market's ticker causes the other, lags, and
	coefficient values for the given lags.

    Each of the corresponding fields listed will be columns for the created table.
    """

	ticker = CharField()
	month = CharField()
	lead = IntegerField()
	causer_NASDAQ = CharField() #changed ITCH to NASDAQ. Variables with "I" correspond to NASDAQ
	lag1_I = FloatField()
	lag2_I = FloatField()
	lag3_I = FloatField()
	lag4_I = FloatField()
	lag5_I = FloatField()
	beta1_I = FloatField()
	beta2_I = FloatField()
	beta3_I = FloatField()
	beta4_I = FloatField()
	beta5_I = FloatField()
	causer_NYSE = CharField()
	lag1_N = FloatField() #vars with '_N' correspond to NYSE
	lag2_N = FloatField()
	lag3_N = FloatField()
	lag4_N = FloatField()
	lag5_N = FloatField()
	beta1_N = FloatField()
	beta2_N = FloatField()
	beta3_N = FloatField()
	beta4_N = FloatField()
	beta5_N = FloatField()


def create_tables():
	"""
    This function will create a table in the database so that data can be read into it.

    First, it will delete the CrossMkt table if that table has already been created.
    Next, it will create a table in the database using the information from the
    CrossMkt class previously defined.
    """
	try:
		CrossMkt.delete()
	except:
		pass
	try:
		db.create_tables([CrossMkt])
		#db.connect()
	except Exception as e:
		print(e)

if __name__ == "__main__":
	create_tables()
	rootCrGc = '../Cross-Market/Granger Causality Tests/'
	#Isolate relevant files
	files = [ rootCrGc + f for f in os.listdir(rootCrGc) if os.path.isfile(rootCrGc + f) ]
	#print(files)
	#Loop through files to populate database table
	for ff in files:
		#print(ff)
		name = ff.split('/')[-1]
		#print(name)
		if name[0:8] == "cross_gc":
			parts = name.split('_')
			month = int(parts[3])
			month_change = {1:'JAN' , 2: 'FEB', 3: 'MAR', 4:'APR', 5:'MAY', 6:'JUN', 7:'JUL',
			8: 'AUG', 9:'SEP', 10:'OCT', 11:'NOV', 12:'DEC'}
			new_month = month_change[month]
			lead_time = parts[4].split(".csv")[0]
			the_file = pd.read_csv(ff)
			the_file.rename(columns={"causer ITCH": "causer_NASDAQ",
			"LI1": "lag1_I", "LI2": "lag2_I", "LI3": "lag3_I",
			"LI4": "lag4_I", "LI5": "lag5_I", "BI1": "beta1_I",
			"BI2": "beta2_I", "BI3": "beta3_I", "BI4": "beta4_I",
			"BI5": "beta5_I", "causer NYSE": "causer_NYSE",
			"LN1": "lag1_N", "LN2": "lag2_N", "LN3": "lag3_N",
			"LN4": "lag4_N", "LN5": "lag5_N", "BN1": "beta1_N",
			"BN2": "beta2_N", "BN3": "beta3_N", "BN4": "beta4_N",
			"BN5": "beta5_N"}, inplace=True)

			ddict = the_file.to_dict(orient="index")
			data = list(ddict.values())
			for dd in data:
				dd['month'] = new_month
				dd['lead'] = lead_time

			with db.atomic():
				for idx in range(0,len(data),30):
					aa = CrossMkt.insert_many(data[idx:idx+30]).execute()
