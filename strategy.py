import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
import yfinance as yf
from bot import buy_stocks, clear, sellStocks 
import pyautogui
import keyboard
import time
from datetime import datetime, timedelta


def wait_until_time(hour, minute):
    while True:
        current_time = datetime.now()
        if current_time.hour == hour and current_time.minute == minute:
            break
        time.sleep(30)

def getTopGainers():
    url = "https://finance.yahoo.com/markets/stocks/gainers/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all("span", class_="symbol yf-1jpysdn")
    symbols = [item.text for item in results]
    return symbols

def getTopLoser():
    url = "https://finance.yahoo.com/markets/stocks/losers/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all("span", class_="symbol yf-1jpysdn")
    symbols = [item.text for item in results]
    return symbols


def getTopGainersInfo(topGainersList, interval, start, end):
    data = yf.download(topGainersList, start=start, end=end,interval=interval)
    df = pd.DataFrame(data=data) 
    return df

def getTopLosersInfo(topLoserList, interval, start, end):
    data = yf.download(topLoserList, start=start, end=end,interval=interval)
    df = pd.DataFrame(data=data) 
    return df

def calculateIncrease(data, start):
    start = data.iloc[start, 0]
    current = data.iloc[len(data) - 1, 0]
    change = (current - start)/start
    change = change *100
    print(change)
    return change

def returnMax(list):
    index = list["Change"].idxmax()
    max = list["Change"].max()
    return(index, max)

def returnMin(list):
    index = list["Change"].idxmin()
    min = list["Change"].min()
    return(index, min)

def cleanUpLoser(df):
    df = df.sort_values(by='Change', ascending=True)
    df['Change'] = df['Change'].round(2)
    return df

def cleanUpGainer(df):
    df = df.sort_values(by='Change', ascending=False)
    df['Change'] = df['Change'].round(2)
    return df

def calcShares(price, goal):
    x = int(goal) / float(price)
    x = round(x)
    x = str(x)
    return x

def calculateStopLoss(price):
    stopLoss = price - (price * 0.07)
    return stopLoss

def closeStocks(file):
    stockToClose = pd.DataFrame(columns=['Ticker', 'Short or Long', 'Shares'])
    df = pd.read_excel(file)
    today = datetime.today().strftime('%Y-%m-%d')
    for index, row in df.iterrows():
        if row['Date'] == today:
            newData = {
                'Ticker': row['Ticker'], 
                'Short or Long': row['Short or Long'],
                'Shares': row['Amounts of share']
            }
            stockToClose = pd.concat([stockToClose, pd.DataFrame([newData])], ignore_index=True)
    
    return stockToClose




def run(gainer, alreadyBought):
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    tomorrow = tomorrow.strftime('%Y-%m-%d')
    today = datetime.today().strftime('%Y-%m-%d')

    buy_type = 'Short' if gainer else 'Long'

    if gainer == True:
        topGainers = getTopGainers()
        rows = []
        for i in topGainers:
            curent = i
            temp = getTopGainersInfo(curent, "1m", today, tomorrow)
            if temp.empty:
                print(f"No data available for {curent}")
                continue
            num = calculateIncrease(temp, 0)
            rows.append([i, num])
        increases = pd.DataFrame(rows, columns=['Stock', 'Change'])
        increases = cleanUpGainer(increases)
        print(increases)
        for i in range(len(increases)):
            temp = getTopGainersInfo(increases.iloc[i,0], "1m", today, tomorrow)
            isIn = increases.iloc[i, 0] in alreadyBought['Ticker'].values
            if not isIn:
                shares = calcShares(temp.iloc[len(temp) - 1, 0], 80000)
                buy_stocks(increases.iloc[i,0], True, shares)
                clear()
                new_data = {
                    'Date': today,
                    'Ticker': increases.iloc[i, 0],
                    'Short or Long': buy_type,
                    'Buying price': float(temp.iloc[len(temp) - 1, 0]),
                    'Amounts of share': shares
                }
                print(new_data)
                alreadyBought = pd.concat([alreadyBought, pd.DataFrame([new_data])], ignore_index=True)
                return alreadyBought
                break

    if gainer == False:
        topLoser = getTopLoser()
        rows = []
        for i in topLoser:
            curent = i
            temp = getTopLosersInfo(curent, "1m", today, tomorrow)
            if temp.empty:
                print(f"No data available for {curent}")
                continue
            num = calculateIncrease(temp, 0)
            rows.append([i, num])
        increases = pd.DataFrame(rows, columns=['Stock', 'Change'])
        increases = cleanUpLoser(increases)
        for i in range(len(increases)):
            temp = getTopGainersInfo(increases.iloc[i,0], "1m", today, tomorrow)
            isIn = increases.iloc[i, 0] in alreadyBought['Ticker'].values
            if not isIn:
                shares = calcShares(temp.iloc[len(temp) - 1, 0], 80000)
                buy_stocks(increases.iloc[i,0], False, shares)
                clear()
                new_data = {
                    'Date' : today,
                    'Ticker': increases.iloc[i, 0],
                    'Short or Long': buy_type,
                    'Buying price': float(temp.iloc[len(temp) - 1, 0]),
                    'Amounts of share': shares
                }
                print(new_data)
                alreadyBought = pd.concat([alreadyBought, pd.DataFrame([new_data])], ignore_index=True)
                return alreadyBought
                break

    

def main():
    i = 0
    alreadyBought = pd.DataFrame(columns=['Date','Ticker', 'Short or Long', 'Buying price', 'Amounts of share'])
    
    while(i <3):
        alreadyBought = run(False, alreadyBought)
        alreadyBought = run(True, alreadyBought)
        i += 1
    print("Stocks bought: ")
    print(alreadyBought)
    df_existing = pd.read_excel('Trading.xlsx')
    df_combined = pd.concat([df_existing, alreadyBought], ignore_index=False)
    df_combined.to_excel('Trading.xlsx', index=False)


main()

'''Fix i gotta make:
- 

New things i gotta make:
- append to excel - done
- close trades
- 
'''





#buy_stocks(topGainers[index], True, "500")
#clear()



# We will create 2 strategies from this
# A full short strategy based on shorting the top gainers of the first minute of the day



# What the code should check

#You should check the volume, bid/ask spread and depth-of-book pre-market. That big price move you are seeing may possibly just be the cost of crossing the spread pre-market. I am guessing this is a big part of the "alpha" you are seeing.
#1#Here's a relatively simple strategy to try to see if you can make money on this:
#
#Calculate market beta on all the stocks you are tracking
#
#See how much the market moved before the open. Perhaps there is a popular index ETF to track the market you are following
#
#Place a limit order to sell short at the open. For each stock, set the limit order to (yesterday's close for stock) * (1.01 + (index's return before open) * (stock's beta to the index)). This basically says that if the stock moved up more than 1% on top of what the market has returned overnight, then sell it short.
#
#Close the position some minutes after the opening bell. Maybe 5?
#
#If it works don't forget who your friends are. Get in touch and I'll tell you where to deliver the yacht.
