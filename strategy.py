# class if all strategies
import pandas as pd
import numpy as np
from pandas_datareader import data

#unecessary imports
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#date set
# start_date = '2018-01-01'
# end_date = '2021-01-01'
# with open('dataset.csv', 'rb') as csvfile:
#   goog_data=csv.reader(csvfile, delimiter=' ', quotechar='|')

def strategy(flag):
#flag is a boolean variable which we can add in future for increasing efficiency
#if function returns -1 do NOTHING
#if function returns 0 SELL
#if function returns 1 BUY\
    goog_data = pd.read_csv("database.csv") 
    #3 moving average
    # fast wala
    ShrortEMA =goog_data.price.ewm(span =2 , adjust = False).mean()
    #medium
    medEMA = goog_data.price.ewm(span = 4 , adjust = False).mean()
    #long
    LongEMA = goog_data.price.ewm(span=8 , adjust=False ).mean()
    #vars 
    goog_data['Short'] = ShrortEMA
    goog_data['Medium']= medEMA
    goog_data['Long'] = LongEMA
    #check
    goog_data['Buy'] = buy_or_sell(goog_data)[0]
    goog_data['Sell'] = buy_or_sell(goog_data)[1]
    #logic
    if goog_data['Sell'].iloc[-1] >= 0:
        if goog_data['Buy'].iloc[-1] >= 0:
            return -1
        else:
            return 1  
    else:
        return 0  

def buy_or_sell(data):
    buy_list =[]
    sell_list = []
    flag_long = False
    flag_short=False

    for i in range(0 , len(data)):
        if data['Medium'][i] < data['Long'][i] and data['Short'][i] < data['Medium'][i] and flag_long == False and flag_short == False:
            buy_list.append(data['price'][i])
            sell_list.append(np.nan)
            flag_short = True
        elif flag_short == True and data['Short'][i]>data['Medium'][i]:
            buy_list.append(np.nan)
            sell_list.append(data['price'][i]) 
            flag_short = False
        elif data['Medium'][i] > data['Long'][i] and data['Short'][i] > data['Medium'][i] and flag_long == False and flag_short == False:
            buy_list.append(data['price'][i])
            sell_list.append(np.nan)
            flag_long = True
        elif flag_long == True and data['Short'][i]<data['Medium'][i]:
            buy_list.append(np.nan)
            sell_list.append(data['price'][i]) 
            flag_long = False 
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)  
    return (buy_list , sell_list)

if __name__=='__main__':
    goog_data = pd.read_csv("database.csv") 
    print(goog_data)
    #plot check
    plt.figure(figsize=(12.2 , 4.5))
    plt.title('price')
    plt.plot(goog_data['price'])
    plt.show()
    #3 moving average
    # fast wala
    ShrortEMA =goog_data.price.ewm(span =2 , adjust = False).mean()
    # #medium
    medEMA = goog_data.price.ewm(span = 4 , adjust = False).mean()
    # #long
    LongEMA = goog_data.price.ewm(span=8 , adjust=False ).mean()

    #display the moving averages
    plt.figure(figsize=(18 , 8))
    plt.title('price')
    plt.plot(goog_data['price'] , label = 'Price', color = 'blue')
    plt.plot(ShrortEMA ,label = 'Short graph', color = 'red')
    plt.plot(LongEMA,label = 'Short graph', color = 'violet')
    plt.plot(medEMA,label = 'Short graph', color = 'green')
    plt.show()

    #The strategy==================================================

    #Algorithm to buy or sell stocks
    #instead off adding data in the list we can use buy sell dummy api to buy/sell stocks
  
    #strategy ends===================================================================================
    #Adding buy sell signals to the dataset
    goog_data['Medium']=medEMA
    goog_data['Short']=ShrortEMA
    goog_data['Long']=LongEMA

    goog_data['Buy'] = buy_or_sell(goog_data)[0]
    goog_data['Sell'] = buy_or_sell(goog_data)[1]

    #display the final buy/sell plot
    plt.figure(figsize=(18 , 8))
    plt.title('Buy Sell Chart')
    plt.plot(goog_data['price'] , label = 'Price', color = 'blue' , alpha=0.35)
    #plt.plot(ShrortEMA ,label = 'Short graph', color = 'red', alpha=0.35)
    #plt.plot(LongEMA,label = 'Short graph', color = 'violet', alpha=0.35)
    #plt.plot(medEMA,label = 'Short graph', color = 'green', alpha=0.35)
    plt.scatter(goog_data.index ,goog_data['Buy'] , color='green' , marker='^' , alpha=1)
    plt.scatter(goog_data.index ,goog_data['Sell'] , color='red' , marker='v' , alpha=1)
    plt.show()
    