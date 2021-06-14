# Option Simple
Semester Project 2021 - Programming

The program aims to create a Graphical User Interface (GUI) that allows you to estimate the price of different options by choosing companies from over 20,000 possible choices. It is also possible to export daily stock prices and returns to an excel file.


## Packages

* pandas – version 1.2.2
* pandasdatareader – version 0.9.0
* numpy – version 1.19.5
* numba – version 0.53.1
* threading – version 3.4
* PyQt5 (Qt) – version 5.15.2
* yahoofinancials – version 1.6
* scipy – version 1.6.1

## Instructions

All files must stay in the same folder for the proper functioning of the program.

To run the program, you should only run de file main.py


## Appendix

The code "Appendix - ticker_cleaner.py" is a prepatory work for the project. 
The goal is to filter the companies that have data available on yahoo finance. 
Thus, we remove tickers of companies that have less than 100 days of historical data or that are not available by the data provider.
