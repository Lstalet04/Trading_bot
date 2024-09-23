import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
import yfinance as yf
from bot import buy_stocks, clear 
import pyautogui
import keyboard

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

def calculateIncrease(data, start, end):
    start = data.iloc[start, 0]
    current = data.iloc[end, 0]
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


topGainers = getTopLoser()

rows = []
for i in topGainers:
    curent = i
    temp = getTopLosersInfo(curent, "1m", "2024-09-23", "2024-09-24")
    num = calculateIncrease(temp, 0, 7)
    rows.append([i, num])
increases = pd.DataFrame(rows, columns=['Stock', 'Change'])
print(increases)
index, maximumChange = returnMin(increases)
buy_stocks(topGainers[index], True, "500")
clear()



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
