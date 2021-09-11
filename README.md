# crypto-ta-bot
Crypto Technical Analysis Bot for Telegram  

This bot allows the price and indicators to be displayed instantly of all coins on Binance using Binance API.

# Supported Indicators

- Relative Strength Index (RSI)  
- Moving Average Convergence Divergence (MACD)  
- Money Flow Index (MFI)  
- Commodity Channel Index (CCI)  
- Bollinger Bands (BB)  
- Simple Moving Average (SMA)  
- Williams %R (%R)  
- Stochastic RSI (STOCH RSI)  
- Average Directional Movement Index (ADX)  

# Commands

/start  
![Ekran görüntüsü 2021-08-14 234506](https://user-images.githubusercontent.com/15037280/129459755-0e6f91de-f18b-4c7d-8914-98f69757de99.png)

/commands  
![Ekran görüntüsü 2021-08-14 225605](https://user-images.githubusercontent.com/15037280/129459774-06678a33-90a8-4bf0-92dd-0a3d271e84eb.png)

/indicator  
![Ekran görüntüsü 2021-09-11 225807](https://user-images.githubusercontent.com/15037280/132960949-068d0110-fdca-4e71-ac9e-8a136aba3cba.png)

/intervals  
![Ekran görüntüsü 2021-08-14 234530](https://user-images.githubusercontent.com/15037280/129459770-25707cdc-0318-4d51-bb64-098e17551ba3.png)

# Installing

Get a Telegram API Key and Binance API Key (they are free).  
Open file named telegram-api.txt with any text editor and paste your Telegram API Key like this  
```sh
yourkey
```
then open another file named binance-api.txt and paste your Binance API Key skip to bottom line and paste your Binance Secret Key.  

It must look like this:
```sh
API Key
Secret Key
```

Run terminal as administrator in folder

First Command:
```sh
pip install -r requirements.txt
```

Second Command:
```sh
py telegram.py
```

after typing second command program should work.  
