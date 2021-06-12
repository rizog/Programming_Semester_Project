# -*- coding: utf-8 -*-
"""
class UITicker
Select ticker
"""

import pandas as pd
import numpy as np

from PyQt5.QtGui import QFontDatabase, QFont, QIcon
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import (QGroupBox,QPushButton, 
                             QVBoxLayout, QHBoxLayout, QWidget)
from PyQt5.QtWidgets import *


class UITicker(QWidget):
    """ Window 2 class : ticker selection """
    
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
        
        # dataframe w/ all tickers
        try:
            self.alltickers # if defined
            
        except:
            # if not defined
            self.alltickers = pd.read_excel("tickDisplay.xlsx", index_col=0)
        
        
        # first horizontal box
        hbox1      = QHBoxLayout() 
        
        self.label_ticker = QLabel("Ticker : ") 
        self.label_ticker.setFont(QFont(self.font, 12))
        hbox1.addWidget(self.label_ticker)
        
        self.edit_ticker = QLineEdit()
        self.edit_ticker.setFont(QFont(self.font, 12))
        hbox1.addWidget(self.edit_ticker)
        
        btn_editTick =  QPushButton("Search (Ctrl+S)")
        btn_editTick.setFont(QFont(self.font, 12))
        btn_editTick.clicked.connect(self.find_item) # linked to the find_item fct
        btn_editTick.setShortcut("Ctrl+S")
        hbox1.addWidget(btn_editTick)
        
        # For the display
        self.listwidget = QListWidget()
        self.total_list = self.alltickers["NameDisplay"].tolist()
        self.listwidget.addItems(self.total_list)  
        
        # used for the search
        self.listwidget2 = QListWidget()
        self.total_list2 = self.alltickers["NameAndTicker"].tolist()
        self.listwidget2.addItems(self.total_list2)
        
        # buttons
        hb = QHBoxLayout()
        
        self.Prev = QPushButton("Prev")
        self.Prev.setFont(QFont(self.font, 18))
        hb.addWidget(self.Prev)
    
        self.button = QPushButton("Save company")
        self.button.clicked.connect(self.display) # display function
        self.button.setFont(QFont(self.font, 18))
        hb.addWidget(self.button)
        
        self.Next = QPushButton('Next')
        self.Next.setEnabled(False) # while ticker not selected, button not enabled
        self.Next.setFont(QFont(self.font, 18))
        hb.addWidget(self.Next)
        
        # integrate all horizontal layers in a vertical layer
        auto_search_vbox = QVBoxLayout(self)
        auto_search_vbox.addLayout(hbox1)
        auto_search_vbox.addWidget(self.listwidget) # ticker list
        auto_search_vbox.addLayout(hb)
   
        # mandatory conversion in order to display the content
        self.widget = QWidget()
        self.widget.setLayout(auto_search_vbox)
        MainWindow.setCentralWidget(self.widget)
        
        
    def find_item(self):
        """ find edit.text in dataframe """
  
        # occurences in listwidget2 for the search edit_ticker (upper)
        out = self.listwidget2.findItems(self.edit_ticker.text().upper(), 
                                        Qt.MatchContains |          # +++
                                        Qt.MatchCaseSensitive)      # +++
        
        list_display = [ i.text() for i in out ] # list with all the occurences
        
        # links the list values to the dataframe rows
        part = self.alltickers.loc[self.alltickers["NameAndTicker"] == list_display[0]]
        for i in range(1, len(list_display)):
            part = part.append(self.alltickers.loc[self.alltickers["NameAndTicker"] == list_display[i]])
    
        # conversion to list in order to display the results
        partList = part["NameDisplay"].tolist()

        self.listwidget.clear() # clear the list displayed
        self.listwidget.addItems(partList) # display the new list generated
        
        
        
    def display(self):
        """ save the ticker and set the button enabled """
        
        SelectedTick = self.listwidget.selectedItems() # line selected
        x = []
        for i in list(SelectedTick):
            x.append(str(i.text())) # get the element, str type in list
            
        # from the line selected, get the ticker    
        tick = self.alltickers.loc[self.alltickers["NameDisplay"] == x[0]]
        tick = tick.index[0]
 
        self.SelectedTicker = tick # add the ticker to the class
        self.SelectedCompany = self.alltickers["Name"][tick] # company name
        self.SelectedCountry = self.alltickers["Country"][tick] # company's country
        self.SelectedExchange = self.alltickers["Exchange"][tick] # company's exchange

        if len(self.SelectedTicker) > 0:
            # if the line selected is not empty
            self.Next.setEnabled(True) # allow the user to click on "next"
    