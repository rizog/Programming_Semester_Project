# -*- coding: utf-8 -*-
"""
Monte-carlo simulation function
"""


#import pandas as pd
import numpy as np
from scipy.stats import norm
import random
from math import exp, sqrt, log
from numba import jit

# import time
# start_time = time.time()

@jit
def monte_carlo_call(spot, strike, maturity, vola, div=0, rf=0.016, sim=10000):
        """ monte carlo simulation for call option """
        K = strike
        sigma = vola
        nsim = sim #  %number of simulations
        
        T = maturity # in years
        n = 30
        r = rf # risk-free rate
        q = div # dividend yield
        s0 = spot  # spot price
        
        x = 120 # number of steps
        dt = T/x # time differential
    
        e = np.random.randn(nsim, x) # normal distribution value 
        z = np.zeros((nsim, x+1)) # initialisation of the brownian motion matrix
        s = np.zeros((nsim,x)) # initialisation of the prices matrix 
       
    
        # brownian motion simulation
        for i in range(0, nsim):
            for j in range(1, x+1): #start from 2, indeed, z0 = 0
                z[i][j] = z[i][j-1] + (r-q-0.5*sigma**2)*dt + sigma*sqrt(dt)*e[i][j-1]
                # nsim lines, 121 columns
    
        # prices simulation
        for i in range(0, nsim):
            for j in range(0, x):
                s[i][j] = s0*exp(z[i][j+1])
                
        # payoff computation 
        s_n = np.zeros((nsim,x)) # initialisation of the matrix which will take only the prices of the last 30 days
        
        for i in range(0, nsim):
            for j in range(0, n):
                s_n[i][j] = s[i][j+(x-n)] # we take only the prices from s91 to s120
        
        s_n_sum = s_n.sum(axis=1)    # sum(s_n,2), sum by row
        maxLeft = (1/n)*(s_n_sum) - K    # df : sum average - K, positive payoff
        payoff = maxLeft.copy()
    
        for L in range(len(payoff)):
            payoff[L] = max(float(maxLeft[L]), 0) # max (S-K, 0)
    
        output = (1/nsim) * np.sum(payoff) * exp(-r*T) # discounted average of payoffs
        # the output will be the price
        return output
        


@jit
def monte_carlo_put(spot, strike, maturity, vola, div=0, rf=0.016, sim=10000):
        """ monte carlo simulation for put option """
        K = strike
        sigma = vola
        nsim = sim #  %number of simulations
        
        T = maturity # in years
        n = 30
        r = rf # risk-free rate
        q = div # dividend yield
        s0 = spot  # spot price
        
        x = 120 # number of steps
        dt = T/x # time differential
    
        e = np.random.randn(nsim, x) # normal distribution value 
        z = np.zeros((nsim, x+1)) # initialisation of the brownian motion matrix
        s = np.zeros((nsim,x)) # initialisation of the prices matrix 
       
        # brownian motion simulation
        for i in range(0, nsim):
            for j in range(1, x+1): #start from 2, indeed, z0 = 0
                z[i][j] = z[i][j-1] + (r-q-0.5*sigma**2)*dt + sigma*sqrt(dt)*e[i][j-1]
    
        # prices simulation
        for i in range(0, nsim):
            for j in range(0, x):
                s[i][j] = s0*exp(z[i][j+1])
                
        # payoff computation 
        s_n = np.zeros((nsim,x)) # initialisation of the matrix which will take only the prices of the last 30 days
        
        for i in range(0, nsim):
            for j in range(0, n):
                s_n[i][j] = s[i][j+(x-n)] # we take only the prices from s91 to s120
        
        s_n_sum = s_n.sum(axis=1)    # sum(s_n,2), sum by row
        maxLeft = K - (1/n)*(s_n_sum) # df : K - sum_average, positive payoff
        payoff = maxLeft.copy()
    
        for L in range(len(payoff)):
            payoff[L] = max(float(maxLeft[L]), 0) # max (S-K, 0)
    
        output = (1/nsim) * np.sum(payoff) * exp(-r*T) # discounted average of payoffs
        # the output will be the price
        return output




#print(monte_carlo_call(100,110,1,0.2)) # test
#print("--- %s seconds ---" % (time.time() - start_time))

# print(monte_carlo_put(100,90,1, 0.2)) # test
# print("--- %s seconds ---" % (time.time() - start_time))