import tornado.ioloop
import tornado.web
import os
from pprint import pprint

import peewee
from peewee import fn
import numpy as np
from gc_data import Asset
from company_data import Company
#from shape_data import Volatility, Midpoint
from shape_data import *
from gc_cross_mkt import CrossMkt
from playhouse.shortcuts import model_to_dict
import json

# The RequestHandler is the base class for HTTP request handlers
class TickerHandler(tornado.web.RequestHandler):

    # Defining "get" requests data from the server
    # Self is used to refer to the object calling the function
    def get(self, tick):
        '''
        Returns JSON object (called 'output' below) with the following properties:

        data       - a list of dictionaries, where each dictionary represents one line
                     from the Asset model in gc_data.db
        meta       - a dictionary of the corresponding line from the Company model in
                     the company_data.db
        rsqrd      - a list of two lists, where the first list is of the mean
                     R-squared for each ticker across all months and the second list
                     is of the standard deviations
        neighbor   - a list of two lists, where the first list is of the average neighbor
                     manipulability score for each ticker in the exchange and lead time
                     specified in the functions file. The second list is the mean R-squared
                     for each ticker in the corresponding exchange and lead time
        cross      - a dictionary of the corresponding line from the CrossMkt model
                     in gc_cross_mkt.db
        vol        - a dictionary from the Volatility model in shape_data.db
        midpoint   - a dictionary from the Midpoint model in shape_data.db
        manip_rank - dictionary with statistics regarding overall manipulability
                     for this month and lead time
                     (keys are 'rank', 'ticker', 'rsqrd')
        '''

        resp = "The request was for ticker {}".format(tick)
        ticker, month, lead = tick.split("/")
        tick = ticker.upper()
        month = month.upper()
        #month_names = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}
        #new_month = month_names[month.lower()]
        #print(new_month)
        lead_change = {'10': 0.05, '60': 60, '600': 600}
        new_lead = lead_change[lead]
        #print(tick, lead, month.lower())
        #res = Asset.select().where((Asset.ticker == tick) & (Asset.month == new_month) & (Asset.lead == lead) )
        res = Asset.select().where((Asset.ticker == tick) & (Asset.lead == lead) & (fn.Lower(fn.Substr(Asset.month,1,3)) == month.lower()))
        out = []
        causers = []
        for rr in res:
            d = model_to_dict(rr)
            pprint(d['causer'])
            try:
                causer_shape = Midpoint.select().where((Midpoint.ticker == d['causer'])  & (Midpoint.lead == new_lead) & (fn.Lower(fn.Substr(Midpoint.month,1,3)) == month.lower())).get()
                d['causer_shape'] = causer_shape.r_squared
            except peewee.DoesNotExist:
                print(d['causer'] + " does not exist--moving on")
            out.append(d)



        # Get company metadata
        cres = Company.select().where((Company.ticker == tick)).get()
        if cres:
            output = {'data': out, 'meta': model_to_dict(cres)}
        if lead == '10':
            rsqrdsmean = [tt.r2mean10 for tt in Company.select(Company.r2mean10) if tt.r2mean10 != None]
            rsqrdsstd = [tt.r2std10 for tt in Company.select(Company.r2std10) if tt.r2std10 != None]
            #join = {'means':rsqrdsmean,'deviations':rsqrdsstd}
            join = [rsqrdsmean,rsqrdsstd]
            #join = np.array(join).T.tolist()
            output['rsqrd'] = join
        elif lead == '60':
            rsqrdsmean = [tt.r2mean60 for tt in Company.select(Company.r2mean60) if tt.r2mean60 != None]
            rsqrdsstd = [tt.r2std60 for tt in Company.select(Company.r2std60) if tt.r2std60 != None]
            #join = {'means':rsqrdsmean,'deviations':rsqrdsstd}
            join = [rsqrdsmean,rsqrdsstd]
            output['rsqrd'] = join
        elif lead == '600':
            rsqrdsmean = [tt.r2mean600 for tt in Company.select(Company.r2mean600) if tt.r2mean600 != None]
            rsqrdsstd = [tt.r2std600 for tt in Company.select(Company.r2std600) if tt.r2std600 != None]
            #join = {'means':rsqrdsmean,'deviations':rsqrdsstd}
            join = [rsqrdsmean,rsqrdsstd]
            output['rsqrd'] = join

        neighbor_manip = [nn.avg_neighbor_manip_score for nn in Company.select(Company.avg_neighbor_manip_score).where(Company.avg_neighbor_manip_score != None)]
        neighbor_rsqrd = [nn.rsqrd_neighbor_plot for nn in Company.select(Company.rsqrd_neighbor_plot).where(Company.avg_neighbor_manip_score != None)]
        output['neighbor'] = [neighbor_manip,neighbor_rsqrd]


        crssres = CrossMkt.select().where((CrossMkt.ticker == tick) & (CrossMkt.lead == lead) & (fn.Lower(fn.Substr(CrossMkt.month,1,3)) == month.lower())).get()
        k =  model_to_dict(crssres)
        shape_cross = Midpoint.select().where((Midpoint.ticker == k['ticker']) & (Midpoint.lead == new_lead) & (fn.Lower(fn.Substr(Midpoint.month,1,3)) == month.lower())).get()
        k['shape'] = shape_cross.r_squared
        if crssres:
            output['cross'] = k

        # While waiting for new regressions, map a lead in the UI to a lead for the shape regressions.
        # Get predictability of volatility
        all_records = Volatility.select()
        for ii in all_records:
            pass
        test_result = Volatility.select().where(Volatility.ticker == tick).get()

        vres = Volatility.select().where((Volatility.ticker == tick) & (Volatility.lead == new_lead) & (fn.Lower(fn.Substr(Volatility.month,1,3)) == month.lower())).get()
        if vres:
            output['vol'] = model_to_dict(vres)



        # Get predictability of future midpoint
        mres = Midpoint.select().where((Midpoint.ticker == tick) & (Midpoint.lead == new_lead) & (fn.Lower(fn.Substr(Midpoint.month,1,3)) == month.lower())).get()
        if mres:
            output['midpoint'] = model_to_dict(mres)

        # Get overall manipulability data for this month and lead
        manip_list = []
        rres = Midpoint.select().where((Midpoint.lead == new_lead) & (fn.Lower(fn.Substr(Midpoint.month,1,3))== month.lower())).order_by(Midpoint.r_squared.desc())
        init_val = 1
        for rr in rres:
            manip_list.append({'rank': init_val,'ticker':  rr.ticker, 'r_squared': rr.r_squared})
            init_val += 1

        output['manip_rank'] = manip_list

        json_data = json.dumps(output)
        self.write(json_data)



class MostManipulableHandler(tornado.web.RequestHandler):
    def get(self,url):
        month, lead = url.split("/")
        print(month,lead)
        month = month.upper()
        lead_change = {'10': 0.05, '60': 60, '600': 600}
        new_lead = lead_change[lead]
        outlist = []
        res = Midpoint.select().where((Midpoint.lead == new_lead) & (fn.Lower(fn.Substr(Midpoint.month,1,3))== month.lower())).order_by(Midpoint.r_squared.desc())
        init_val = 1
        for rr in res:
            outlist.append({'rank': init_val,'ticker':  rr.ticker, 'r_squared': rr.r_squared})
            init_val += 1

        json_data = json.dumps(outlist)
        self.write(json_data)

class SuggestionHandler(tornado.web.RequestHandler):
    def get(self, sugg):
        outlist = []
        res = Company.select().where((Company.ticker.contains(sugg) | (Company.Name==sugg)))
        for rr in res:
            dd = model_to_dict(rr)
            outlist.append(dd)

        json_data = json.dumps(outlist)
        self.write(json_data)


root = os.path.dirname(os.path.realpath(__file__))

application = tornado.web.Application([
    (r"/ticker/(.*)", TickerHandler),
    (r"/suggest/(.*)", SuggestionHandler),
    (r"/mm/(.*)", MostManipulableHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": root, "default_filename": r"index.html"}),], debug=True)



if __name__ == "__main__":
    """
    x = Asset.select().where(Asset.ticker == "AAPL").get()
    print(x)
    y = Company.select().where(Company.ticker.contains("AAPL"))
    for cc in y:
        print(cc)
    """
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
