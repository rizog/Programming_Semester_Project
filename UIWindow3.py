# -*- coding: utf-8 -*-
"""
class UIWindow3
display the third window
"""

########### PACKAGES ###########
from datetime import date
import dateutil.relativedelta
from yahoofinancials import YahooFinancials
import pandas as pd
import numpy as np
import sys


from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFontDatabase, QFont, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import (QCheckBox, QGridLayout, QGroupBox,
        QMenu, QPushButton, QRadioButton, QComboBox, QVBoxLayout, QHBoxLayout, QWidget,
        QCalendarWidget)
from PyQt5.QtWidgets import *
import pandas_datareader.data as web
import datetime as dt
from datetime import date

##################################

class UIWindow3(QWidget):
    """ Third window : select the strike price and the periode in months """
    
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
        
        
        try:
            if self.SelectedTicker == "Nan":
                print("No ticker")

        except:
            print("ticker not defined")
            self.SelectedTicker = "Nan"
        
        
        ### to display the spot price
        start = dt.datetime(2021, 5, 5)
        end = date.today()  
        prices = web.DataReader(self.SelectedTicker, 'yahoo', start=start, end=end)['Adj Close']
        self.spot = round(prices[-1], 2)
        ###
        
    
        # horizontal box bottom with buttons
        hb = QHBoxLayout()
        self.Prev = QPushButton("Prev") # Previous
        self.Prev.setFont(QFont(self.font, 18))
        
        self.button_save = QPushButton("Save")
        self.button_save.clicked.connect(self.save) # function save
        self.button_save.setFont(QFont(self.font, 18))
        
        self.Next = QPushButton('Next')
        self.Next.setEnabled(False)
        self.Next.setFont(QFont(self.font, 18))
        
        hb.addWidget(self.Prev)
        hb.addWidget(self.button_save)
        hb.addWidget(self.Next)
        
      
        """
        Layout construction
        0. selected stock, spot price --> group_summary
        1. combo box - option type --> comboLayout
        2. strike price and error handing --> group_K_Layout
        3. calendar and slider for the maturity --> slider_Layout
        4. button
        """
        
        W3_grid = QGridLayout()
        W3_grid.addWidget(self.group_summary(), 0, 0)
        W3_grid.addWidget(self.comboLayout(), 1, 0)
        W3_grid.addWidget(self.group_K_Layout(), 2, 0)
        W3_grid.addWidget(self.slider_Layout(), 3, 0)
        W3_grid.addLayout(hb, 4, 0)
        
        
        self.widget = QWidget()
        self.widget.setLayout(W3_grid)
        MainWindow.setCentralWidget(self.widget)
        
        

        
    def group_summary(self):
        self.group_sum = QGroupBox("Selected ticker and spot price")
        self.group_sum.setFont(QFont(self.font, 12))
        vbox_sum = QVBoxLayout()
        
        # horizontal box top
        htop = QHBoxLayout()
        self.label_tick = QLabel("Selected stock : ")
        self.label_tick.setFont(QFont(self.font, 12))
        self.display_tick = QLabel(str(self.SelectedTicker))
        self.display_tick.setFont(QFont(self.font, 12))
        htop.addWidget(self.label_tick)
        htop.addWidget(self.display_tick)
        
        # horizonal box 2 (spot price)
        htop2 = QHBoxLayout()
        str_spot = str(self.spot)
        self.label_spot = QLabel("Spot price : ")
        self.label_spot.setFont(QFont(self.font, 12))
        
        self.display_spot = QLabel(str_spot)
        self.display_spot.setFont(QFont(self.font, 12))
        htop2.addWidget(self.label_spot)
        htop2.addWidget(self.display_spot)
        
        vbox_sum.addLayout(htop)
        vbox_sum.addLayout(htop2)
        self.group_sum.setLayout(vbox_sum)
        return self.group_sum
       
        
    def changeValue(self, value):
        """ add slider value to the class and display the value in term of month-year """
        self.valueSlider = value
        self.label_slider.setText(self.convert_int_to_period()) # change text
        self.label_slider.adjustSize()
        
    def convert_int_to_period(self):
        """ function to display value of the slider """
        today = date.today() # date today
        maturity = today + dateutil.relativedelta.relativedelta(months=self.valueSlider)
        maturity_display = maturity.strftime("%b %y")
        return maturity_display
    
    def comboLayout(self):
        self.group_combo = QGroupBox("Select the option type")
        self.group_combo.setFont(QFont(self.font, 12))
        
        hm0 = QHBoxLayout()
        self.label_option = QLabel("Option type : ")
        self.label_option.setFont(QFont(self.font, 12))
        self.combo = QComboBox()
        self.combo.addItem("European call")
        self.combo.addItem("European put")
        self.combo.addItem("Asian call")
        self.combo.addItem("Asian put")
        self.combo.setFont(QFont(QFont(self.font, 12)))
        hm0.addWidget(self.label_option)
        hm0.addWidget(self.combo)       
        
        self.group_combo.setLayout(hm0)
        return self.group_combo
        
    
    def group_K_Layout(self):
        self.group_K = QGroupBox("Strike price")
        self.group_K.setFont(QFont(self.font, 12))
        vbox_K = QVBoxLayout()
        
        hme = QHBoxLayout()
        self.label_K_Error = QLabel() # defined in function save
        self.label_K_Error.setFont(QFont(self.font, 12))
        self.label_K_Error.setStyleSheet('color: red')
        hme.addWidget(self.label_K_Error)
        
        # horizontal box middle 1
        hm = QHBoxLayout()
        self.label_K = QLabel("Strike price : ")
        self.label_K.setFont(QFont(self.font, 12))
        self.edit_K = QLineEdit()   
        self.edit_K.setFont(QFont(self.font, 12))
        hm.addWidget(self.label_K)
        hm.addWidget(self.edit_K)
        
        vbox_K.addLayout(hme)
        vbox_K.addLayout(hm)
        self.group_K.setLayout(vbox_K)
        return self.group_K
        
     
    
    def slider_Layout(self):
        self.group_slider = QGroupBox("Start date to export the data, and the option maturity")
        self.group_slider.setFont(QFont(self.font, 12))
        
        self.cal = QCalendarWidget() # calendar
        today = date.today()
        fiveYearsAgo = today - dateutil.relativedelta.relativedelta(months=12*5)
        self.cal.setSelectedDate(fiveYearsAgo)
        
        time_v = QVBoxLayout()
        time_v.addWidget(self.cal)
        
        hm2 = QHBoxLayout()
        self.label_maturity = QLabel("Maturity:")
        self.label_maturity.setFont(QFont(self.font, 12))
        hm2.addWidget(self.label_maturity)
        
        self.Slider = QSlider(Qt.Horizontal, self) # slider, in months
        self.Slider.setGeometry(300, 480, 400, 300)
        self.Slider.setMaximum(18) # = 18 months
        self.Slider.setMinimum(1)
        self.Slider.setValue(1) # 12 month
        self.Slider.valueChanged[int].connect(self.changeValue) # function changeValue
        hm2.addWidget(self.Slider)
         
        maturity = today + dateutil.relativedelta.relativedelta(months=1)
        maturity_display = maturity.strftime("%b %y")
        self.label_slider = QLabel(maturity_display)
        self.label_slider.setFont(QFont(self.font, 12))
        hm2.addWidget(self.label_slider)
        hm2.addWidget(self.Slider)
        
        time_v.addLayout(hm2)
        self.group_slider.setLayout(time_v)
        
        return self.group_slider
    
    def save(self):
        """ if 'save' is clicked """
        try:
            self.K = float(self.edit_K.text()) # convert the strike price
            assert self.K > 0 # the strike price should be positive
            
            self.months = self.valueSlider
            self.option_type = str(self.combo.currentText())
            
            self.start_date = self.cal.selectedDate().toPyDate()
            self.Next.setEnabled(True) # allow to click on next
            
        except ValueError:
            # if the input of strike price is not a float
            #print("Value error: UIWindow3 save")
            self.label_K_Error.setText("This strike price is not a float")
            self.label_K_Error.adjustSize()
        
        except AttributeError:
            #print("Attribut error: UIWindow3 save")
            # self.valueSlider not defined
            # = the user did not move the Slider
            # = take initial value = 1 months
            self.valueSlider = 1
            
            self.K = float(self.edit_K.text())
            self.months = self.valueSlider
            self.option_type = str(self.combo.currentText())
            
            self.start_date = self.cal.selectedDate().toPyDate()
            self.Next.setEnabled(True)
            
        except AssertionError:
            # if the strike price is not positive
            self.label_K_Error.setText("The strike price is not positive")
            self.label_K_Error.adjustSize()
            
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        

        