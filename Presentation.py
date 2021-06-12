# -*- coding: utf-8 -*-
"""
class Presentation 
Window 1
"""

########### PACKAGES ###########
import sys
import pandas as pd
import numpy as np


from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFontDatabase, QFont, QStandardItemModel, QStandardItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider
from PyQt5.QtWidgets import (QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QRadioButton, 
                             QVBoxLayout, QHBoxLayout, QWidget)
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtWidgets import *

##################################




class Presentation(object):
    """ Presentation class : the first window """
    
    def setupUI(self, MainWindow):
        #### window parameters
        self.title = "Option Pricing"
        self.iconName = "logo.png"
        self.left = 450
        self.top = 200
        self.width = 1000
        self.height = 800
        
        MainWindow.setGeometry(self.left, self.top,self.width,self.height) # window size
        MainWindow.setFixedSize(self.width,self.height)
        MainWindow.setWindowTitle(self.title) # window title
        MainWindow.setWindowIcon(QIcon(self.iconName))
        
        
        # Presentation text
        self.explainations = QLabel("Welcome to Option Simple! "\
                                    "\n\nThis software gives you the opportunity "\
                                    "to compute option prices  of "\
                                    "\nmore than 20,000 companies  and to download financial data."\
                                    "\n\nThis software is developed as part of the semestrial project in "\
                                    "\nthe Programming course." )

        self.explainations.setFont(QFont("Roboto", 15)) # text option (font and size)


        self.label = QLabel()
        pixmap = QPixmap("logo_p.png") # the logo in the window
        pixmap = pixmap.scaled(400, 400)
        self.label.setPixmap(pixmap)


        
        self.Next = QPushButton("Next") # button to the second window
        self.Next.setFont(QFont("Roboto", 18))
        
        
        presentation_vbox = QVBoxLayout() # vertical layout
        h1 = QHBoxLayout() # first horizontal box inside the vertical layout
        h1.addWidget(self.label)
        h1.setContentsMargins(310, 0, 310, 0) #L, Top, R, Bottom

        h12 = QHBoxLayout() # second horizontal box inside the vertical layout
        h12.addWidget(self.explainations)
        h12.setContentsMargins(100, 0, 100, 0)
        
        presentation_vbox.addLayout(h1)
        presentation_vbox.addLayout(h12)

        h2 = QHBoxLayout() # second horizontal box inside the vertical layout
        h2.addWidget(self.Next)
        self.Next.setEnabled(False) # disable the button while the data is not loaded
        presentation_vbox.addLayout(h2)
        
        # mandatory conversion in order to display the content
        self.widget = QWidget()
        self.widget.setLayout(presentation_vbox)
        MainWindow.setCentralWidget(self.widget)
        