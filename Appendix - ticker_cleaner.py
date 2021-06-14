# -*- coding: utf-8 -*-
"""
This file concerns the preparatory work of the project.
The goal is to filter the companies that have data available on yahoo finance

"""

import pandas as pd
import numpy as np
from datetime import date
import dateutil.relativedelta
from yahoofinancials import YahooFinancials

import logging
import threading
import time




today = date.today()  # date
today_str = today.strftime("%Y-%m-%y") # change date format

start = today - dateutil.relativedelta.relativedelta(months=5*12) # five years ago
start = start.strftime("%Y-%m-%y")


alltickers = pd.read_excel("tick.xlsx") # this is the excel sheet with all the companies and tickers (+100'000)



def price_generator(start, end, tick, periods):
        """ generate daily prices and returns from yahoo """
        tickers = [tick]
        tick_yahoo = YahooFinancials(tickers)
        data = tick_yahoo.get_historical_price_data(start, 
                                                     end, 
                                                     periods)
        
        df = pd.DataFrame({
            a: {x['formatted_date']: x['adjclose'] for x in data[a]['prices']} for a in tickers})
        
        prices = df.dropna()
        return prices
   


x = alltickers.copy()
x["verif"] = 1 # in the dataframe, the column "verif" is equal to 1 if the ticker is valid
# else, the value is 0 (if it is not possible to use the ticker of if there is less than 100 days in historical data)


# thread 1
def thread1():
	""" function for the first thread
	--> even indexes """
    global x
    for i in range(0,110001, 2):
    	# from 0 to 110,000, 2 by 2
        if (i-0)%10 == 0:
            print("\nthread 1 : ", i,"\n")
            # every 10 indexes, print i in order to know at which step the hread is
            
        tick = x.iloc[i, 0] # the ticker
        try:
            prices = price_generator(start, today_str, tick, "daily")

            if len(prices) < 100:
            	# if there is less than 100 days
                x["verif"][i] = 0
            
        except:
        	# if an error occur
            x["verif"][i] = 0
    


# thread 2, same but odds numbers
def thread2():
    global x
    for k in range(1,110002,2):
        if (k-1)%10 == 0:
            print("\nthread 2 : ", k,"\n")
            
        tick = x.iloc[k, 0] # the ticker
        try:
            prices = price_generator(start, today_str, tick, "daily")

            if len(prices) < 100:
                x["verif"][k] = 0
            
        except:
            x["verif"][k] = 0
    



# define 2 threads
t1 = threading.Thread(target=thread1) 
t2 = threading.Thread(target=thread2)     
    
# start
t1.start()
t2.start()

# join
t1.join()
t2.join()
    