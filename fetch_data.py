import pandas as pd
import datetime
import time
#from bitmex import bitmex
from binance.client import Client #pip install python-binance
from pandas.core.frame import DataFrame
import requests
import json
from datetime import timedelta, datetime
from dateutil import parser
from tqdm import tqdm_notebook #(Optional, used for progress-bars) #pip install tqdm
import math
import os.path

#My Imports
from config import *





### CONSTANTS
binsizes = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}
batch_size = 750
#bitmex_client = bitmex(test=False, api_key=bitmex_api_key, api_secret=bitmex_api_secret)
binance_client = Client(api_key=binance_api_key, api_secret=binance_api_secret)


### FUNCTIONS
def minutes_of_new_data(symbol, kline_size, data, source):
    if len(data) > 0:  old = parser.parse(data["timestamp"].iloc[-1])
    elif source == "binance": old = datetime.strptime('1 Jan 2017', '%d %b %Y')
    #elif source == "bitmex": old = bitmex_client.Trade.Trade_getBucketed(symbol=symbol, binSize=kline_size, count=1, reverse=False).result()[0][0]['timestamp']
    if source == "binance": new = pd.to_datetime(binance_client.get_klines(symbol=symbol, interval=kline_size)[-1][0], unit='ms')
    #if source == "bitmex": new = bitmex_client.Trade.Trade_getBucketed(symbol=symbol, binSize=kline_size, count=1, reverse=True).result()[0][0]['timestamp']
    return old, new

def get_all_binance(symbol, kline_size):
    filename = '%s-%s-data.csv' % (symbol, kline_size)
    if os.path.isfile(filename): 
        print('Found '+filename)
        data_df = pd.read_csv(filename)
        data_df = data_df.drop_duplicates(subset=['timestamp'])
    else: 
        data_df = pd.DataFrame()
    oldest_point, newest_point = minutes_of_new_data(symbol, kline_size, data_df, source = "binance")
    delta_min = (newest_point - oldest_point).total_seconds()/60
    available_data = math.ceil(delta_min/binsizes[kline_size])
    if oldest_point == datetime.strptime('1 Jan 2017', '%d %b %Y'): 
        print('Downloading all available %s data for %s. Be patient..!' % (kline_size, symbol))
    elif delta_min == 0:
        print('No new data available')
        return
    else: 
        print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data.' % (delta_min, symbol, available_data, kline_size))
    #klines = binance_client.get_historical_klines(symbol, kline_size, oldest_point.strftime("%d %b %Y %H:%M:%S"), newest_point.strftime("%d %b %Y %H:%M:%S"))  
    klines = binance_client.get_historical_klines(symbol, kline_size, str(datetime.strptime('30 May 2021 12:40:00', "%d %b %Y %H:%M:%S")), newest_point.strftime("%d %b %Y %H:%M:%S"))    
    print('Data received')
    data = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    #if len(data_df) > 0:
    #    temp_df = pd.DataFrame(data)
    #    data_df = data_df.append(temp_df)
    #else: data_df = data
    data_df = data
    data_df.set_index('timestamp', inplace=True)
    data_df.to_csv(filename)        
    return filename

"""
def get_all_bitmex(symbol, kline_size, save = False):
    filename = '%s-%s-data.csv' % (symbol, kline_size)
    if os.path.isfile(filename): data_df = pd.read_csv(filename)
    else: data_df = pd.DataFrame()
    oldest_point, newest_point = minutes_of_new_data(symbol, kline_size, data_df, source = "bitmex")
    delta_min = (newest_point - oldest_point).total_seconds()/60
    available_data = math.ceil(delta_min/binsizes[kline_size])
    rounds = math.ceil(available_data / batch_size)
    if rounds > 0:
        print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data in %d rounds.' % (delta_min, symbol, available_data, kline_size, rounds))
        for round_num in tqdm_notebook(range(rounds)):
            time.sleep(1)
            new_time = (oldest_point + timedelta(minutes = round_num * batch_size * binsizes[kline_size]))
            data = bitmex_client.Trade.Trade_getBucketed(symbol=symbol, binSize=kline_size, count=batch_size, startTime = new_time).result()[0]
            temp_df = pd.DataFrame(data)
            data_df = data_df.append(temp_df)
    data_df.set_index('timestamp', inplace=True)
    if save and rounds > 0: data_df.to_csv(filename)
    print('All caught up..!')
    return data_df


"""



#interval = '1d' # 1d, 1m
#ticker = 'BTC'
# yb = year base, mob = month base...yf = year final
def fetch_yahoo(ticker, interval, yb, mob, db, hb, mb, yf, mof, df, hf, mf):    
    period1 = int(time.mktime(datetime.datetime(yb, mob, db, hb, mb).timetuple()))
    period2 = int(time.mktime(datetime.datetime(yf, mof, df, hf, mf).timetuple()))
    
    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
    print(query_string)
    df = pd.read_csv(query_string)
    df = df.sort_values('Date')
    del df['Adj Close']

    csv_fname = "yahoo_data_"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".csv"    
    df.to_csv(csv_fname)
    print(csv_fname)
    return csv_fname

#import json

def fetch_rapidapi(stock, interval):
    url = "https://twelve-data1.p.rapidapi.com/time_series"

    #querystring = {"currency_base":stock,"interval":interval,"format":"json"}
    querystring = {"symbol":"AMZN","interval":"1day","outputsize":"30","format":"json"}

    headers = {
        'x-rapidapi-key': "28dcb4926dmsh556aaf516249f58p1301ddjsnbfc7c062b894",
        'x-rapidapi-host': "twelve-data1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response)
    df = DataFrame(response)
    df.to_csv("rapidapi_"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".csv")
      
    
    

#fetch_yahoo('AAPL', '1d', 2020,10,10,10,10,2020,10,16,3,3)