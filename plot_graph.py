from matplotlib.pyplot import axes, title, xlabel
import pandas as pd  #pip install pandas-datareader
import mplfinance as mpf  #pip install --upgrade mplfinance
import matplotlib.animation as animation 
import datetime
from datetime import date, datetime


#My Imports
from utils import *
from config import *

s = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 10})
fig = mpf.figure(style=s,figsize=(10,11))
fig.suptitle(trading_bot_version, fontsize=16)
#Placing on figure section
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(3,1,3)
#fig.patch.set_facecolor('black')

csv = None


def animateAndShow(ival):

	print('Opening .csv '+csv)
	idf = pd.read_csv(csv)
	time_frame = None
	#Time chart frame	
	idf['timestamp'] = pd.to_datetime(idf['timestamp'], format='%Y-%m-%d %H:%M:%S')			
	idf.index = pd.DatetimeIndex(idf['timestamp'])
	#Plotting graph
	ax1.clear
	ax2.clear
	mpf.plot(idf, ax=ax1, type='candle', mav=(9), volume=ax2, ylabel='Price US$',block=False,returnfig=True,axtitle='BTC')

def animate(csv_file):
	global csv
	csv = csv_file
	ani = animation.FuncAnimation(fig, animateAndShow, interval=250)
	mpf.show()
