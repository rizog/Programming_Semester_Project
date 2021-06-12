# -*- coding: utf-8 -*-
"""
Black and Scholes function
"""

import numpy as np
from scipy.stats import norm



def BS_call(spot, strike, maturity, vola, q=0, r = 0.016):
        """ 
        Black and Scholes
        r is the risk-free rate. Default value = US 10Y treasury yield
        q is the dividend yield
        """
        
        S = spot
        K = strike
        T = maturity
        sigma = vola
        
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
    
        call = (S *np.exp(-q * T)* norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * norm.cdf(d2, 0.0, 1.0))
    
        return call
    
    
def BS_put(spot, strike, maturity, vola, q=0, r = 0.016):
        """ 
        Black and Scholes
        r is the risk-free rate. Default value = US 10Y treasury yield
        q is the dividend yield
        """
        
        S = spot
        K = strike
        T = maturity
        sigma = vola
        
        
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        put = (K * np.exp(-r * T) * norm.cdf(-d2, 0.0, 1.0)) - S*norm.cdf(-d1, 0.0, 1.0)*np.exp(-q * T)
        
    
        return put