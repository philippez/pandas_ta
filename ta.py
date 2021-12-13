import ccxt, yfinance
import pandas_ta as ta
import pandas as pd
import requests

exchange = ccxt.binance()

bars = exchange.fetch_ohlcv('ETH/USDC', timeframe='5m', limit=500)

df = pd.DataFrame(bars, columns = ['time', 'open', 'high', 'low', 'close', 'volume'])

# adx = ta.adx(df['high'], df['low'], df['close'])
adx = df.ta.adx()

macd = df.ta.macd(fast=14, slow=28)

rsi = df.ta.rsi()

# print(adx)
# print(macd)
# print(rsi)

df_concat = pd.concat([df, adx, macd, rsi], axis = 1)

# print(df_concat)

#print(df)

# ticker = yfinance.Ticker("HOOD")
# df_hood = ticker.history(period="1y")

# print(df_hood)

WEBHOOK_URL = 'https://discord.com/api/webhooks/919952241929097226/rgF_EmybEpzQ3Oi3uEEdDwS6RfafREiLWzna8gpAv2P3y2pVVnTS1BDzG9ZBg0bZfMXv'

last_row = df_concat.iloc[-1]

print(last_row)

if last_row['ADX_14'] >= 25:
    if last_row['DMP_14'] > last_row['DMN_14']:
        message = f"STRONG UPTREND: The ADX is {last_row['ADX_14']}"
        print(message)
    if last_row['DMN_14'] > last_row['DMP_14']:
        message = f"STRONG DOWNTREND: The ADX is {last_row['ADX_14']}"
        print(message)
if last_row['ADX_14'] < 25:
    message = f"NO TREND: The ADX is {last_row['ADX_14']}"
    print(message)

payload = {
    "username": "alertbot",
    "content": message
}

requests.post(WEBHOOK_URL, json=payload)

