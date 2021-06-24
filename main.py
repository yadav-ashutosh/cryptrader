# running strategies and sending broker signal every time new price is appended to db

import os
from binance.client import Client
import numpy as np
import pandas as pd
from strategy import *
from datetime import datetime
import time
import math

def main(client):

    action=strategy('ok')
    order=None

    if action==0:
        buy_order = client.client.create_test_order(symbol='BTCUSDT', side='BUY', type='MARKET', quantity=0.1)
        order=buy_order
    elif action ==1:
        sell_order = client.client.create_test_order(symbol='BTCUSDT', side='SELL', type='MARKET', quantity=0.1)
        order=sell_order

    print(action)

    btc_df=pd.read_csv('database.csv')
    btc_df.at[len(btc_df)-1,'action']=action
    btc_df.to_csv('database.csv',index=False)

    return order
    

if __name__=='__main__':
    pass
   # on database update:
  #      action = strategy(params)
 #       call_api_binance(action)
#        update action column in database















