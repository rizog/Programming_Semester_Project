# -*- coding: utf-8 -*-
"""
class Result
Window 4
"""

#### Import packages
from datetime import date
import dateutil.relativedelta
from yahoofinancials import YahooFinancials
import pandas as pd
import numpy as np

from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, 
                             QHBoxLayout, QWidget, QFileDialog, QTabWidget, QWidget)
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from scipy.stats import norm
import random
from math import exp, sqrt, log

from monte_carlo import monte_carlo_call, monte_carlo_put
from BlackAndScholes import BS_call, BS_put

##################################

class UIWindow4(object):
    """ Window 4 : display results and export data """
    
    def setupUI(self, MainWindow):
        # window parameters
        self.title = "Option Pricing"
        self.iconName = "logo.png"
        self.left = 450
        self.top = 200
        self.width = 1000
        self.height = 800
        self.font = "Roboto"
        
        MainWindow.setGeometry(self.left, self.top,self.width,self.height) # window size
        MainWindow.setFixedSize(self.width,self.height)
        MainWindow.setWindowTitle(self.title) # window title
        MainWindow.setWindowIcon(QIcon(self.iconName))
        
        
        # set the date today and x month ago
        today = date.today()    
        T = today + dateutil.relativedelta.relativedelta(months=self.valueSlider) # maturity

        self.T_scaled = self.valueSlider / 12 # scale the maturity in years for the computations
        # for example, 12 months = 1 year

        
        start = self.start_date.strftime("%Y-%m-%y") # to download data and compute volatility
        today_str = today.strftime("%Y-%m-%y") # change date format
        T_display = T.strftime("%b %y")
        
        self.price_generator(start, today_str, "daily") # function to generate stock price
        
        # compute the  annualized daily returns volatility
        self.vola = float(self.returns.std() * np.power(21*12, 0.5)) 
        # assume 21 * 12 trading days
        
        
        """
        all the lines in summary
        
        """
        
        # Ticker selected
        h1 = QHBoxLayout()      
        self.label_ticker = QLabel("Ticker : ")
        self.label_ticker.setFont(QFont(self.font, 12))
        self.display_ticker = QLabel(self.SelectedTicker)
        self.display_ticker.setFont(QFont(self.font, 12))
        h1.addWidget(self.label_ticker)
        h1.addWidget(self.display_ticker)
        
        # company name
        h2 = QHBoxLayout()  
        self.label_company = QLabel("Company name : ")
        self.label_company.setFont(QFont(self.font, 12))
        self.display_company = QLabel(self.SelectedCompany)
        self.display_company.setFont(QFont(self.font, 12))
        h2.addWidget(self.label_company)
        h2.addWidget(self.display_company)
        
        # country
        h22 = QHBoxLayout()  
        self.label_country = QLabel("Country : ")
        self.label_country.setFont(QFont(self.font, 12))
        self.display_country = QLabel(self.SelectedCountry)
        self.display_country.setFont(QFont(self.font, 12))
        h22.addWidget(self.label_country)
        h22.addWidget(self.display_country)
        
        # Stock exchange
        h23 = QHBoxLayout()  
        self.label_exchange = QLabel("Exchange : ")
        self.label_exchange.setFont(QFont(self.font, 12))
        self.display_exchange = QLabel(self.SelectedExchange)
        self.display_exchange.setFont(QFont(self.font, 12))
        h23.addWidget(self.label_exchange)
        h23.addWidget(self.display_exchange)
        
        # dividend yield
        h24 = QHBoxLayout()  
        self.label_dividend = QLabel("Dividend yield : ")
        self.label_dividend.setFont(QFont(self.font, 12))
        str_div = "{} %".format(str(round(self.div_yield*100,2)))
        self.display_dividend = QLabel(str_div)
        self.display_dividend.setFont(QFont(self.font, 12))
        h24.addWidget(self.label_dividend)
        h24.addWidget(self.display_dividend)
        
        # option type
        h25 = QHBoxLayout()  
        self.label_option_type = QLabel("Option type : ")
        self.label_option_type.setFont(QFont(self.font, 12))
        self.display_option_type = QLabel(self.option_type)
        self.display_option_type.setFont(QFont(self.font, 12))
        h25.addWidget(self.label_option_type)
        h25.addWidget(self.display_option_type)
        
        # strike price
        h3 = QHBoxLayout()  
        self.label_strike = QLabel("Strike price : ")
        self.label_strike.setFont(QFont(self.font, 12))
        self.display_strike = QLabel(str(self.K))
        self.display_strike.setFont(QFont(self.font, 12))
        h3.addWidget(self.label_strike)
        h3.addWidget(self.display_strike)
        
        # maturity
        h32 = QHBoxLayout()  
        self.label_maturity = QLabel("Maturity : ")
        self.label_maturity.setFont(QFont(self.font, 12))
        self.display_maturity = QLabel(T_display)
        self.display_maturity.setFont(QFont(self.font, 12))
        h32.addWidget(self.label_maturity)
        h32.addWidget(self.display_maturity)
        
        # spot price
        h4 = QHBoxLayout()  
        self.label_spot = QLabel("Spot price : ")
        self.label_spot.setFont(QFont(self.font, 12))
        self.S0 = float(self.prices.iloc[-1,0]) # the last price
        
        self.display_spot = QLabel(str(round(self.S0,2)))
        self.display_spot.setFont(QFont(self.font, 12))
        h4.addWidget(self.label_spot)
        h4.addWidget(self.display_spot)
        
        # volatility
        h5 = QHBoxLayout()  
        self.label_volatility = QLabel("Volatility : ")
        self.label_volatility.setFont(QFont(self.font, 12))
        str_vola = "{} %".format(str(round(self.vola*100, 2)))
        self.display_volatility = QLabel(str_vola)
        self.display_volatility.setFont(QFont(self.font, 12))
        h5.addWidget(self.label_volatility)
        h5.addWidget(self.display_volatility)
        
        # Option price
        h6 = QHBoxLayout()  
        self.label_option_price = QLabel("Option price : ")
        self.label_option_price.setFont(QFont(self.font, 12))
        self.display_option_price = QLabel() # defined in function
        self.display_option_price.setFont(QFont(self.font, 12))
        h6.addWidget(self.label_option_price)
        h6.addWidget(self.display_option_price)
    
        # buttons to compute the option price and export dataframe
        h7 = QHBoxLayout() 
        self.button_compute = QPushButton("Compute")
        self.button_compute.setFont(QFont(self.font, 18))
        self.button_compute.clicked.connect(self.compute) # function
    
        self.button_export = QPushButton("Export")
        self.button_export.setFont(QFont(self.font, 18))
        self.button_export.clicked.connect(self.export) # function
        h7.addWidget(self.button_compute)
        h7.addWidget(self.button_export)
   
        self.Prev = QPushButton("Prev")
        self.Prev.setFont(QFont(self.font, 18))
        
        # combine all these lines in a vertical layout
        window4_vbox = QVBoxLayout()
        window4_vbox.addLayout(h1)
        window4_vbox.addLayout(h2)
        window4_vbox.addLayout(h22)
        window4_vbox.addLayout(h23)
        window4_vbox.addLayout(h24)
        window4_vbox.addLayout(h25)
        window4_vbox.addLayout(h3)
        window4_vbox.addLayout(h32)
        window4_vbox.addLayout(h4)
        window4_vbox.addLayout(h5)
        window4_vbox.addLayout(h6)


        ####
        # Tab widget
        # first tab : option pricing
        # second tab : chart of the price
        
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        
        self.tabs.addTab(self.tab1,"Option pricing")
        self.tabs.addTab(self.tab2,"Chart")
        
        self.tab1.setLayout(window4_vbox)
        
        self.sc = MplCanvas(self, width=5, height=4, dpi=100) # canvas
        
        self.prices[self.SelectedTicker].plot(ax=self.sc.axes, title=self.SelectedCompany) # chart
        toolbar = NavigationToolbar(self.sc, self.tab1) # toolbar for the chart

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)
        widget_chart = QWidget()
        widget_chart.setLayout(layout)
        self.tab2.setLayout(layout)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabs)
        self.layout.addLayout(h7) # compute, export
        self.layout.addWidget(self.Prev)
        
        ####
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        MainWindow.setCentralWidget(self.widget)
        
        
    def price_generator(self, start, end, periods):
        """ generate daily prices and returns from yahoo """
        tickers = [self.SelectedTicker]
        tick_yahoo = YahooFinancials(tickers)
        data = tick_yahoo.get_historical_price_data(start, 
                                                     end, 
                                                     periods)
        
        df = pd.DataFrame({
            a: {x['formatted_date']: x['adjclose'] for x in data[a]['prices']} for a in tickers})
        
        self.prices = df.dropna()
        self.returns = self.prices.pct_change().dropna()
        try:
            self.div_yield = tick_yahoo.get_dividend_yield()
            #print(self.div_yield[self.SelectedTicker])
            if self.div_yield[self.SelectedTicker] == None:
                self.div_yield = 0.00
            else:
                self.div_yield = self.div_yield[self.SelectedTicker]
        except:
            print("no dividend yield")
        
        
    def compute(self):
        """ run the monte-carlo simulation
        or the Black and Scholes function
        we use a risk-free rate of 1.6% which is the yield of a 10Y treasury on may 2021 """
        
        if self.option_type == "European call":
            option_price = BS_call(self.S0, self.K, self.T_scaled, self.vola, self.div_yield, r=0.016)
        
        elif self.option_type == "European put":
            option_price = BS_put(self.S0, self.K, self.T_scaled, self.vola, self.div_yield,  r=0.016)
        
        elif self.option_type ==  "Asian call":
            option_price = monte_carlo_call(self.S0, self.K, self.T_scaled, self.vola, self.div_yield, rf=0.016 ) # function in other file
        else:
            # Asian put
            option_price = monte_carlo_put(self.S0, self.K, self.T_scaled, self.vola, self.div_yield, rf=0.016)
        

        self.display_option_price.setText(str(round(option_price,2)))
        self.display_option_price.adjustSize()
        
    def export(self):
        """ export the dataframe to excel file """
        self.prices["returns"] = self.returns
        self.prices.columns = ['prices', 'returns']
        self.prices = self.prices.dropna()
        
        name = QFileDialog.getSaveFileName(None, 'Save File', filter='*.xlsx')
        if(name[0] == ''):
            # if name empty
            pass
        else:
            self.prices.to_excel(name[0])   
        

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
    