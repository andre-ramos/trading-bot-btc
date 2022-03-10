import time


#My Imports
from fetch_data import *
from plot_graph import *
from utils import *

class MyThreading:

    csv = None

    def getData(binance_symbols, time_frame):   
        while True:     
            for symbol in binance_symbols:
                    global csv
                    csv = get_all_binance(symbol, time_frame)

   # def plotGraphRealTime():  
       # global csv       
        #animate(csv, TimeFrame.timestamp)

