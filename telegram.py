import telebot
from binance.client import Client
import talib as ta
import numpy as np
import os 

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)

class Trader:
    def __init__(self, file):
        self.connect(file)

    def connect(self,file):
        lines = [line.rstrip('\n') for line in open(file)]
        key = lines[0]
        secret = lines[1]
        self.client = Client(key, secret)

filename = 'binance-api.txt'
trader = Trader(filename)

@bot.message_handler(commands=['commands'])
def commands(message):
    bot.send_message(message.chat.id, ('*Bot Commands:' '\n' '/start' '\n' '/intervals' '\n' '/indicator*'),parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id, ('*Hello !' '\n''\n' 'This bot allows the price and indicators to be displayed instantly on all coins on Binance with using Binance API.' '\n' 'You can find commands in /commands' '\n''\n' 'Check out:* https://github.com/veyasins/crypto-technicalanalysis-bot'),parse_mode="Markdown")

@bot.message_handler(commands=['intervals'])
def intervals(message):
    bot.send_message(message.chat.id, ('*Valid Intervals:*' '\n''1m''\n' '3m''\n' '5m''\n' '15m' '\n''30m''\n' '1h''\n' '2h''\n' '4h''\n' '6h''\n' '8h''\n' '12h''\n' '1d''\n' '3d''\n' '1w''\n''1M'),parse_mode="Markdown")
        
@bot.message_handler(commands=["indicator"])
def send_price(message):
    crypto = message.text.split()[1].upper()
    time = message.text.split()[2].lower()

    symbol = crypto
    interval = time
    klines = trader.client.get_klines(symbol=symbol,interval=interval)

    open = [float(entry[1]) for entry in klines]
    high = [float(entry[2]) for entry in klines]
    low = [float(entry[3]) for entry in klines]
    close = [float(entry[4]) for entry in klines]
    volume = [float(entry[5]) for entry in klines]
    close_array = np.asarray(close)

    #### INDICATORS
    mfi = ta.MFI(high=np.array(high, dtype=float), low=np.array(low, dtype=float),close=np.array(close, dtype=float), volume=np.array(volume, dtype=float), timeperiod=14)[-1]
    cci = ta.CCI(high=np.array(high, dtype=float), low=np.array(low, dtype=float),close=np.array(close, dtype=float), timeperiod=20)[-1]
    rsi = ta.RSI(close_array, timeperiod=14)
    macd, macdsignal, macdhist = ta.MACD(close_array, fastperiod=12, slowperiod=26, signalperiod=9)
    upper, middle, lower = ta.BBANDS(close_array, timeperiod=20, nbdevup=2, nbdevdn=2)
    ema55 = ta.EMA(close_array, timeperiod=55)[-1]
    ema200 = ta.EMA(close_array, timeperiod=200)[-1]
    sma55 = ta.SMA(close_array, timeperiod=55)[-1]
    sma200 = ta.SMA(close_array, timeperiod=200)[-1]
    williams = ta.WILLR(high=np.array(high, dtype=float), low=np.array(low, dtype=float),close=np.array(close, dtype=float), timeperiod=14)[-1]
    srsi = np.asarray(rsi)
    stochrsik, stochrsid = ta.STOCH(srsi,srsi,srsi, fastk_period=14, slowk_period=3, slowd_period=3)

    data = {'‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ':  symbol,'Price': [close_array[-1]],'RSI': [rsi[-1]],'MACD Histogram' : [macdhist[-1]],'MACD Line' : [macd[-1]],'MACD Signal Line' : [macdsignal[-1]],'MFI' : [mfi],'CCI': [cci],'BB UPPER': [upper[-1]],'BB MA': [middle[-1]],'BB LOWER': [lower[-1]],'EMA 55': [ema55],'EMA 200': [ema200],'SMA 55': [sma55],'SMA 200': [sma200],'WILLR': [williams],'Stoch RSI K': [stochrsik[-1]],'Stoch RSI D': [stochrsid[-1]]}

    yazi = ''
    for x in data:
        sayitoyazi = str(data[x])
        if(x!="‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ "):
            yazihali =   sayitoyazi[1:len(sayitoyazi)-1]
            yazi = yazi + '*' + str(x) + ': ' + '*' + yazihali + '\n'
        else:
            yazi = yazi + str(x)  + '   ' + '*' + data[x] + ' on Binance - ' + interval + '*' + '\n'

    bot.send_message(message.chat.id , yazi, parse_mode="Markdown" )

bot.polling()          