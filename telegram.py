import telebot
from binance.client import Client
import talib as ta
import numpy as np

with open('telegram-api.txt') as api:
    api_key = api.read()
    
bot = telebot.TeleBot(api_key)

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
exchange_info = trader.client.get_exchange_info()

@bot.message_handler(commands=['commands'])
def commands(message):
    bot.send_message(message.chat.id, ('*Bot Commands:' '\n' '/start' '\n' '/intervals' '\n' '/indicator*'),parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id, ('*Hello !' '\n''\n' 'This bot allows the price and indicators to be displayed instantly on all coins on Binance with using Binance API.' '\n' 'You can find commands in /commands' '\n''\n' 'Check out:* https://github.com/veyasins/crypto-technicalanalysis-bot'),parse_mode="Markdown")

@bot.message_handler(commands=['intervals'])
def intervals(message):
    bot.send_message(message.chat.id, ('*Valid Intervals:*' '\n''1m''\n' '3m''\n' '5m''\n' '15m' '\n''30m''\n' '1h''\n' '2h''\n' '4h''\n' '6h''\n' '8h''\n' '12h''\n' '1d''\n' '3d''\n' '1w''\n''1M'),parse_mode="Markdown")

def checker(message):
    if len(message.text.split()) == 3:
        coinname = message.text.split()[1].upper()
        wordcount = len(message.text.split())
        command = message.text.split()[0].lower()
        time = message.text.split()[2]
        intervals = ['1m' , '3m', '5m' , '15m' , '30m' , '1h' , '2h' , '4h' , '6h' , '8h' , '12h' , '1d' , '3d' , '1w' , '1M']

        for s in exchange_info['symbols']:
            if coinname == (s['symbol']) and wordcount == 3 and command == '/indicator' and time in intervals:
                return True
            else:
                pass
    else:
        pass

@bot.message_handler(func=checker)
def send_price(message):
    crypto = message.text.split()[1].upper()
    time = message.text.split()[2].lower()
    symbol = crypto
    interval = time
    klines = trader.client.get_klines(symbol=symbol,interval=interval)
    high = [float(entry[2]) for entry in klines]
    low = [float(entry[3]) for entry in klines]
    close = [float(entry[4]) for entry in klines]
    volume = [float(entry[5]) for entry in klines]
    close_array = np.asarray(close)
    dailyopen = [float(entry[1]) for entry in trader.client.get_klines(symbol=symbol,interval='1d')]
    
    if close[-1] > dailyopen[-1]:
        diff = close[-1]-dailyopen[-1]
        formula = (diff/close[-1])*100
        price = '*+'+(str(diff).split('.')[0]+'.'+str(diff).split('.')[1][:3])+' (+'+(str(formula).split('.')[0]+'.'+str(formula).split('.')[1][:2])+'%)*'
    else:
        diff = dailyopen[-1]-close[-1]
        formula = 100-(close[-1]*100/dailyopen[-1])
        price = '*-'+(str(diff).split('.')[0]+'.'+str(diff).split('.')[1][:3])+' (-'+(str(formula).split('.')[0]+'.'+str(formula).split('.')[1][:2])+'%)*'

    mfi = ta.MFI(high=np.array(high, dtype=float), low=np.array(low, dtype=float),close=np.array(close, dtype=float), volume=np.array(volume, dtype=float), timeperiod=14)[-1]
    cci = ta.CCI(high=np.array(high, dtype=float), low=np.array(low, dtype=float),close=np.array(close, dtype=float), timeperiod=20)[-1]
    rsi = ta.RSI(close_array, timeperiod=14)
    macd, macdsignal, macdhist = ta.MACD(close_array, fastperiod=12, slowperiod=26, signalperiod=9)
    upper, middle, lower = ta.BBANDS(close_array, timeperiod=20, nbdevup=2, nbdevdn=2)
    sma50 = ta.SMA(close_array, timeperiod=50)[-1]
    williams = ta.WILLR(high=np.array(high, dtype=float), low=np.array(low, dtype=float),close=np.array(close, dtype=float), timeperiod=14)[-1]
    srsi = np.asarray(rsi)
    stochrsik, stochrsid = ta.STOCH(srsi,srsi,srsi, fastk_period=14, slowk_period=3, slowd_period=3)
    adx = ta.ADX(high=np.array(high, dtype=float), low=np.array(low, dtype=float), close=np.array(close, dtype=float), timeperiod=14)
    data = {'‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ':  symbol,'Price': [str(close_array[-1])+'$  '+price] ,'RSI': [rsi[-1]],'MACD' : [macdhist[-1]],'MFI' : [mfi],'CCI': [cci],'BB': [middle[-1]],'SMA 50': [str(sma50)],'WILL %R': [williams],'Stoch RSI': [stochrsik[-1]],'ADX': [adx[-1]]}
    indlist = [ (str(close_array[-1])+'$  '+price), str(rsi[-1]), str(macdhist[-1]), str(mfi), str(cci), str(middle[-1]), str(sma50), str(williams),str(stochrsik[-1]), str(adx[-1])]

    ozelListemiz = []
    for indicator in indlist:
        splitted = indicator.split(".")     
        sonsayi = "" 
        if(int(splitted[0]) == 0):
            for element in range(0, len(splitted[1])):
              if(int(splitted[1][element]) > 0):

                sonsayi = splitted[1][:element+2]
                ozelListemiz.append([splitted[0],sonsayi]);
                break
        else:
            sonsayi = splitted[1][:2]
            ozelListemiz.append([splitted[0],sonsayi]);
    
    listnum = 0
    yazi = ''
    for x in data:
        numtostr = str(data[x])
        if(x!="‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ "):
            yazihali =   numtostr[1:len(numtostr)-1]
            yazi = yazi + '*' + str(x) + ': ' + '*' + ozelListemiz[listnum][0] + "." + ozelListemiz[listnum][1] 
            if(x=="Price"):
                if(1==1):
                    yazi = yazi +'$  '+price + "\n"
            if(x=="RSI"):
                if(data[x][0] < 30):
                    yazi = yazi + " - *Buy* \n"
                elif (data[x][0] > 70 ):
                    yazi = yazi + " - *Sell* \n"    
                elif (data[x][0] > 30 and data[x][0] < 70):
                    yazi = yazi + " - *Notr* \n"
            if(x=="MACD"):
                if macd[-1] > macdsignal[-1] and macd[-2] < macdsignal[-2]:
                    yazi = yazi + " - Bullish Crossover \n"
                elif macd[-1] < macdsignal[-1] and macd[-2] > macdsignal[-2]:
                    yazi = yazi + " - *Bearish Crossover* \n"
                else:
                    yazi = yazi + " - *Notr* \n"
            if(x=="MFI"):
                if(data[x][0] < 20):
                    yazi = yazi + " - *Buy* \n"
                elif (data[x][0] > 80 ):
                    yazi = yazi + " - *Sell* \n"    
                elif (data[x][0] > 20 and data[x][0] < 80):
                    yazi = yazi + " - *Notr* \n"
            if(x=="CCI"):
                if(data[x][0] < -100):
                    yazi = yazi + " - *Buy* \n"
                elif (data[x][0] > 100 ):
                    yazi = yazi + " - *Sell* \n"
                elif (data[x][0] > -100 and data[x][0] < 100):
                    yazi = yazi + " - *Notr* \n"
            if(x=="BB"):
                if (str(close[-1]) > str(upper[-1])):
                    yazi = yazi + " - *Sell* \n"
                elif (str(close[-1]) < str(lower[-1])):
                    yazi = yazi + " - *Buy* \n"
                elif (str(lower[-1]) < str(close[-1]) < str(middle[-1]) and close[-1] <= (middle[-1] - (middle[-1]-lower[-1] )*0.65) ):
                    yazi = yazi + " - *Near Lower Band* \n"
                elif (str(upper[-1]) > str(close[-1]) > str(middle[-1]) and close[-1] >= (upper[-1] - (upper[-1]-middle[-1] )*0.45)):
                    yazi = yazi + " - *Near Upper Band* \n"
                else:
                    yazi = yazi + " - *Normal* \n"            
            if(x=="SMA 50"):
                if(data[x][0] < str(close[-1])):
                    yazi = yazi + " - *Price is under SMA* \n"
                elif (data[x][0] > str(close[-1]) ):
                    yazi = yazi + " - *Price is above SMA* \n"
            if(x=="WILL %R"):
                if(data[x][0] < -80):
                    yazi = yazi + " - *Buy* \n"
                elif (data[x][0] > -20 ):
                    yazi = yazi + " - *Sell* \n"
                elif (data[x][0] > -80 and data[x][0] < -20):
                    yazi = yazi + " - *Notr* \n"
            if(x=="Stoch RSI"):
                if(data[x][0] < 20):
                    yazi = yazi + " - *Buy* \n"
                elif (data[x][0] > 80 ):
                    yazi = yazi + " - *Sell* \n"
                elif (data[x][0] > 20 and data[x][0] < 80):
                    yazi = yazi + " - *Notr* \n"
            if(x=="ADX"):
                if(data[x][0] < 25):
                    yazi = yazi + " - *Weak Trend* \n"
                elif (data[x][0] > 60 ):
                    yazi = yazi + " - *Very Strong Trend* \n"
                elif (data[x][0] > 25 and data[x][0] < 50):
                    yazi = yazi + " - *Strong Trend* \n"                
                pass
            if(listnum<=len(ozelListemiz)-2):
                listnum+=1
        else:
            yazi = yazi + str(x)  + '   ' + '*' + data[x] + ' on Binance - ' + interval + '*' + '\n'
    bot.send_message(message.chat.id , yazi.replace("'",""), parse_mode="Markdown" )

bot.polling()          
