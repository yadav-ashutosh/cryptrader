# in this file we subscribe to realtime api for price 

import os
from binance.client import Client
import numpy as np
import pandas as pd
#import btalib
from datetime import datetime
import time
import math

#init the binance test api keys
api_key = 'Yle1i6iRKbbvx2YMsIjczwHIV3tthRAO3X3MLNe5wbE24f4mTQr26gY8M7DD8wWY'
secret_key = '4JLW7Tkj3xe2k6MOeqluwITVKAFlEbTlvnRQyRtss5RPxF0V5ylGtyhCRHmkknWi'

# wrapper for time syncing
class Binance:
    def __init__(self, public_key = api_key, secret_key = secret_key, sync = False):
        self.time_offset = 0
        self.client = Client(public_key, secret_key)
        self.client.API_URL = 'https://testnet.binance.vision/api'

        if sync:
            self.time_offset = self._get_time_offset()

    def _get_time_offset(self):
        res = self.client.get_server_time()
        return res['serverTime'] - int(time.time() * 1000)

    def synced(self, fn_name, **args):
        args['timestamp'] = int(time.time() - self.time_offset)
        return getattr(self.client, fn_name)(**args)

if __name__=='__main__':

    client = Binance(sync=True)

    for i in range(10):

        #print(client.synced('get_asset_balance',asset='BTC'))# testing
        
        if 'database.csv' not in os.listdir('.'):
            btc_df = pd.DataFrame(columns=['date', 'price'])
            btc_df.set_index('date', inplace=True)
            btc_df.to_csv('database.csv',index=False)
            
        # getting live price and timestamp

        current_price=client.client.get_symbol_ticker(symbol="BTCUSDT") 
        srv_time=client.client.get_server_time()
        cur_time=time.time()
        timestamp=datetime.fromtimestamp(int(srv_time['serverTime']/1000))
        
        # time to make a pandas df and append price and timestamps to it

        btc_df=pd.read_csv('database.csv')
        btc_df=btc_df.append({'date':timestamp,'price':current_price['price']},ignore_index=True)
        btc_df.to_csv('database.csv',index=False)
        
        time.sleep(1)
   











    #timestamp = client.client._get_earliest_valid_timestamp('BTCUSDT', '1m')
    #print(timestamp)
    #bars = client.client.get_historical_klines('BTCUSDT', '2h', timestamp, limit=18)

    #for line in bars:
    #    del line[5:]

    #btc_df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])
    #btc_df.set_index('date', inplace=True)
    #btc_df.index = pd.to_datetime(btc_df.index, unit='ms')
    #btc_df['20sma']=btc_df.close.rolling(10).mean()
    #print(btc_df.head())
    #print(len(btc_df))