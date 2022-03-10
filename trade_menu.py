from time import sleep
import tkinter as tk
from tkinter import font as tkFont
import importlib
from threading import Thread
from matplotlib.pyplot import plot


#My Imports
from trade_menu import *
from utils import *
from threads import *


#def click(): action.configure(text = "Confirmar") 

#action = tk.Button(text = "Click Me", command = click )
#action.pack()


def print_selection(var1, var2):
    #
    #l = tk.Label(window, bg='white', width=20, text='empty')
    #l.pack()
    #if (var1.get() == 1) & (var2.get() == 0):
    #    l.config(text='BTC')
    #elif (var1.get() == 0) & (var2.get() == 1):
    #    l.config(text='I love C++')
    #elif (var1.get() == 0) & (var2.get() == 0):
    #    l.config(text='I do not anything')
    #else:
    #    l.config(text='I love both')
    print()

def windowSetUp():
    window = tk.Tk()
    window.title('TradeBot')
    window.geometry('400x400')
 
    
    var1 = tk.IntVar()
    var2 = tk.IntVar()
    #size
    helv36 = tkFont.Font(family='Helvetica', size=36, weight=tkFont.BOLD)
    c1 = tk.Checkbutton(window, text='BTC',variable=var1, onvalue=1, offvalue=0, command=print_selection(var1, var2))
    c1.pack()
    c2 = tk.Checkbutton(window, text='DOGE',variable=var2, onvalue=1, offvalue=0, command=print_selection(var1, var2),font=helv36)
    c2.pack()
      
    window.mainloop()
 

def main():
    print('Inicio Robot')
    #csv = fetch_yahoo('AAPL', '5m', 2020,10,10,10,10,2020,10,20,3,3)
    #fetch_rapidapi('BTC/USD',TimeFrame.m5.value)
    #animate(csv, TimeFrame.Day)
    # For Binance

    getDataThread = Thread(target=MyThreading.getData,args=[["BTCUSDT"],TimeFrame.m5.value])
    #plotGraphThread = Thread(target=MyThreading.plotGraphRealTime,args=[])

    getDataThread.start()
    sleep(1)
    animate("BTCUSDT-5m-data.csv")
    #plotGraphThread.start()

    """ esperando threads finalizarem
    threads = []
    threads.append(thread1)
    threads.append(thread2)

    for t in threads:
    t.join()
    """



if __name__ == "__main__":
    main()
