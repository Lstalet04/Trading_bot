import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
import yfinance as yf
from bot import buy_stocks, clear 
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
    results = soup.find_all("span", class_="symbol yf-ravs5v")
    symbols = [item.text for item in results]
    return symbols

def getTopLoser():
    url = "https://finance.yahoo.com/markets/stocks/losers/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all("span", class_="symbol yf-ravs5v")
    print (results)
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
    x = goal / price
    x = str(x)
    return x


def run(gainer,alreadyBought):
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    tomorrow = tomorrow.strftime('%Y-%m-%d')
    today = datetime.today().strftime('%Y-%m-%d')
    if gainer == True:
        topGainers = getTopGainers()
        rows = []
        for i in topGainers:
            curent = i
            temp = getTopGainersInfo(curent, "1m", today, tomorrow)
            if temp.empty:
                print(f"No data available for {curent}")
                continue
            print(temp)
            num = calculateIncrease(temp, 0)
            rows.append([i, num])
        increases = pd.DataFrame(rows, columns=['Stock', 'Change'])
        increases = cleanUpGainer(increases)
        for i in range(len(increases)):
            if alreadyBought.count(increases.iloc[i,0]) == 0:
                buy_stocks(increases.iloc[i,0], True, "500")
                clear()
                alreadyBought.append(increases.iloc[i,0])
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
            print(temp)
            num = calculateIncrease(temp, 0)
            rows.append([i, num])
        increases = pd.DataFrame(rows, columns=['Stock', 'Change'])
        increases = cleanUpLoser(increases)
        for i in range(len(increases)):
            if alreadyBought.count(increases.iloc[i,0]) == 0:
                buy_stocks(increases.iloc[i,0], True, "500")
                clear()
                alreadyBought.append(increases.iloc[i,0])
                break
    

def main():
    i = 0
    alreadyBought = []
    wait_until_time(15, 32)
    while(i <3):
        run(True, alreadyBought)
        run(False, alreadyBought)

main()





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
