# -*- coding: utf-8 -*-
"""
switch between activities
"""

########### PACKAGES ###########
import sys
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import (QPushButton, QWidget)
from PyQt5.QtWidgets import *

# from other files
from UITicker import UITicker
from Presentation import Presentation
from UIWindow3 import UIWindow3
from UIWindow4 import UIWindow4

import threading
#################################


def import_excel():
    """ function used in the thread
    import the excel sheet with all the tickers and company names"""
    global allticks # global to acceed from the class
    allticks = pd.read_excel("tickDisplay.xlsx", index_col=0)
        
global t1 # global to acceed in the class
t1 = threading.Thread(target=import_excel) 
# to display the window and import the data at the same moment
t1.start()


        
class MainWindow(QMainWindow):
    """ main window, allows to switch activities """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # first, we define Class instances for each windows
        self.uiPresentation = Presentation()
        self.uiTicker = UITicker()
        self.uiWindow3 = UIWindow3()
        self.uiWindow4 = UIWindow4()
        
        self.startPresentation() # launch window 1 : presentation
        
        
    def startPresentation(self):
        """ init window 1 : Presentation """
        self.uiPresentation.setupUI(self) # launch the activity
        self.uiPresentation.Next.clicked.connect(self.startUITicker)
        # if "Next" is selected, the second activity starts
        self.show() # display the activity
        t1.join() # join the thread (import data)
        self.uiPresentation.alltickers = allticks # add to the instance
        self.uiPresentation.Next.setEnabled(True) # allow the user to start an other activity
        
        
    def startUITicker(self):
        """ init window 2 : ticker selection """
        self.uiTicker.alltickers = self.uiPresentation.alltickers
        # intent extra from uiPresentation to uiTicker (dataframe w/ all tickers)
        
        self.uiTicker.setupUI(self)
        self.uiTicker.Next.clicked.connect(self.startUIWindow3) # Next
        self.uiTicker.Prev.clicked.connect(self.startPresentation) # Previous
        self.show()   
        
        
    def startUIWindow3(self):
        """ init window 3 : period, strike price, option type, maturity """
        try:
            self.uiWindow3.SelectedTicker = self.uiTicker.SelectedTicker
            # ticker is defined
 
        except:
            print("Unexpected error:", sys.exc_info()[0]) # print error
            # ticker is not defined
            self.uiWindow3.SelectedTicker = "Nan"
        
        self.uiWindow3.setupUI(self)
        self.uiWindow3.Prev.clicked.connect(self.startUITicker)
        self.uiWindow3.Next.clicked.connect(self.startUIWindow4)
        self.show()
        
    
    def startUIWindow4(self):
        """ init window 4 : summary, option pricing, export """
        ### intent extra between activities ###
        # dataframe w/ all tickers
        self.uiWindow4.alltickers = self.uiPresentation.alltickers
        # the ticker selected
        self.uiWindow4.SelectedTicker = self.uiTicker.SelectedTicker
        # company name
        self.uiWindow4.SelectedCompany = self.uiTicker.SelectedCompany
        # country 
        self.uiWindow4.SelectedCountry = self.uiTicker.SelectedCountry
        # exchange
        self.uiWindow4.SelectedExchange = self.uiTicker.SelectedExchange
        # option type
        self.uiWindow4.option_type = self.uiWindow3.option_type
        # strike price
        self.uiWindow4.K = self.uiWindow3.K
        # slider value = number of months
        self.uiWindow4.valueSlider = self.uiWindow3.valueSlider
        # starting date
        self.uiWindow4.start_date = self.uiWindow3.start_date

        self.uiWindow4.setupUI(self)
        self.uiWindow4.Prev.clicked.connect(self.startUIWindow3)
        self.show()  

