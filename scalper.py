import requests
import alpaca_trade_api as tradeapi
import time
import datetime as dt
import tkinter as tk
import threading

import math
import sys

SIREN=ord('🚨')
print(SIREN)

class App():
    def __init__(self):
        url='https://api.alpaca.markets'
        apiID='your key' #get it from your Alpaca brokerage account
        secret='your secret key' #get it from your Alpaca brokerage account
        self.api=tradeapi.REST(apiID, secret, url, 'v2')
        self.cash=float(self.api.get_account().cash) #available cash in your alpaca account
        print(self.cash)
        dts=self.api.get_account().daytrade_count
        if dts>=3:
            sys.exit("You have used all your daytrades")
        self.loop()

    def loop(self):
        while True:
            post=self.get_post()
            if post==None:
                time.sleep(18)
                continue
            text=post['body']
            seconds=self.howLongAgo(post)
            if seconds<6: #we only buy the stock if we catch his tweet within 6 seconds of him posting. Can make this lower if you want the bot to be less aggressive
                print("under 6")
                if self.check_if_alert(text)==True:
                    ticker=self.find_ticker(text)
                    price=self.api.polygon.last_quote(ticker).askprice
                    q=math.floor(self.cash/price) #amount we will buy
                    print("ORDERING AT", dt.datetime.now())
                    self.api.submit_order(
                        symbol=ticker,
                        side='buy',
                        type='market',
                        qty=str(q),
                        time_in_force='day',
                        order_class='bracket',
                        take_profit={
                            'limit_price':str(price*1.03), #take profits at 3% gain
                        },
                        stop_loss={
                            'stop_price':str(price*.97), #stop loss triggers at 3% loss
                            'limit_price':str(price*.96), #sells at 4% loss
                        }
                    )
                    print("ORDERED AT", dt.datetime.now())
                    self.print_prices(ticker)
                    break
            print(text)
            print()
            time.sleep(18)


    def get_post(self):
        try:
            response=requests.get("https://api.stocktwits.com/api/2/streams/user/mrinvestorpro.json")
            message=response.json()['messages'][0]
        except:
            return None
        return message

    def check_if_alert(self, message):
    """Not every post of mrinvestorpro is an alert. His alerts usually contain at least two siren emojis. He also sometimes uses these if he says he's buying more of something,
    but we don't want to count the those, so we make sure the word 'add' is not present"""
        count=0
        sirens=False
        for c in message:
            if ord(c)==SIREN:
                count+=1
        if count>=2:
            sirens=True
        alert=False
        if message.find("add")==-1:
            alert=True
        if sirens==True and alert==True:
            return True
        return False

    def find_ticker(self, message):
        dollar_index=message.find('$')
        space_index=message.find(' ', dollar_index+1)
        ticker=message[dollar_index+1:space_index]
        return ticker

    def print_prices(self, ticker):
        for i in range(50):
            print(dt.datetime.now(), self.api.polygon.last_quote(ticker).askprice)
            time.sleep(1)

    def howLongAgo(self, message):
    """returns how long ago the tweet was posted in seconds"""
        timeString=message['created_at']
        print(timeString)
        now=dt.datetime.now(dt.timezone.utc)
        s=int(timeString[17:19])
        mi=int(timeString[14:16])
        h=int(timeString[11:13])
        y=int(timeString[0:4])
        m=int(timeString[5:7])
        d=int(timeString[8:10])
        tweetTime=dt.datetime(year=y, month=m, day=d, hour=h, minute=mi, second=s, tzinfo=dt.timezone.utc)
        print("now", now)
        print("tweet", tweetTime)
        difference=(now-tweetTime).seconds
        print(difference, 'seconds ago')
        return difference

a=App()
