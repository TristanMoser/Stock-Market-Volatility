
from gc_data import *
from shape_data import *
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict


# Generate the distribution of shape causality r_squared s
def get_rsq_hist(month, lead, filename):
    r = Midpoint.select().where((Midpoint.month == "SEP") & (Midpoint.lead == lead))
    rvec = []
    for rr in r:
        if rr.r_squared is not None:
            rvec.append(rr.r_squared)


    rsq = np.array(rvec)
    print(lead)
    print("mean: {}".format(np.mean(rsq)))
    print("sd: {}".format(np.std(rsq, ddof=1)))


    plt.figure(figsize=(12,5))
    n, bins, patches = plt.hist(rvec, 80, facecolor="#FF3D7F", edgecolor=None)
    plt.savefig(filename, transparent=True)


# Generate the distribution of granger causality params

def get_gc_rsq_hist(month, lead, filename):
    r = Asset.select().where((Asset.month == "SEP") & (Asset.lead == lead))
    rvec = []
    tickers = defaultdict(int)
    for rr in r:
        this_ticker = rr.ticker
        #the_max = max([rr.lag1, rr.lag2, rr.lag3, rr.lag4, rr.lag5])
        the_max = rr.lag1
        tickers[this_ticker] = max(tickers[this_ticker], the_max)



    # Get the fraction with a causer
    total_tickers = len(list(tickers.keys()))
    num_with_causer = 0
    for ii,jj in tickers.items():
        if jj > 0:
            num_with_causer += 1


    frac_with_causer = float(num_with_causer)/total_tickers
    print("frac_with_causer: {}".format(frac_with_causer))







#get_rsq_hist("SEP", 0.05, "lead0_05hist.png")
#get_rsq_hist("SEP", 60, "lead60hist.png")
#get_rsq_hist("SEP", 300, "lead300hist.png")


#get_gc_rsq_hist("SEP", 60, "gc60hist.png")
# Find examples for display.

# First one with high mmidpoint causality and low volatility causality


big_msg = Midpoint.select().where((Midpoint.month == "SEP") & (Midpoint.lead == 60)).order_by(-Midpoint.num_messages)
#for bb in big_msg:
#    print(bb.ticker)

big_r_sq = Midpoint.select().where((Midpoint.month == "SEP") & (Midpoint.lead == 60)).order_by(-Midpoint.r_squared)
for bb in big_r_sq:
    print(bb.ticker)
