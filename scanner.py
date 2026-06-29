import pandas as pd
import yfinance as yf
import requests
from datetime import date

BOT_TOKEN = "8729984501:AAGxp-9ceA4tBGVPm0fHAr--bgkzTbke8zA"
CHAT_ID = "499306024"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# TEMP sample stocks (we will expand later)
symbols = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS"]

results = []

for stock in symbols:
    df = yf.download(stock, period="max", progress=False)

    if df.empty:
        continue

   high = df["High"]
close = df["Close"]

if hasattr(high, "columns"):
    high = high.iloc[:, 0]

if hasattr(close, "columns"):
    close = close.iloc[:, 0]

ath = float(high.max())
current = float(close.iloc[-1])

    down = float(((ath - current) / ath) * 100)

    if 44 <= down <= 46:
        print(stock, down)
