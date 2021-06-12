# -*- coding: utf-8 -*-
"""
Main.py
program starting point
"""

### import packages
import sys
import os 
from PyQt5.QtWidgets import QApplication, QStyleFactory
from class_bot import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # the style changes depending on the OS
    if "Fusion" in [st for st in QStyleFactory.keys()]:
        app.setStyle(QStyleFactory.create("Fusion"))
    elif sys.platform=="win32":
        app.setStyle(QStyleFactory.create("WindowsVista"))
    elif sys.platform=="linux":
        app.setStyle(QStyleFactory.create("gtk"))
    elif sys.platform=="darwin":    
        app.setStyle(QStyleFactory.create("macintosh"))
 
    app.setPalette(QApplication.style().standardPalette())
    
    
    
    w = MainWindow() # class in class_bot file
    sys.exit(app.exec_())
    
        

