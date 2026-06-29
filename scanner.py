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

    ath = df["High"].max()
    current = df["Close"].iloc[-1]

    down = ((ath - current) / ath) * 100

    if 44 <= down <= 46:
        results.append((stock, round(down, 2)))

if results:
    msg = "📊 STOCKS NEAR 45% BELOW ATH\n\n"
    for r in results:
        msg += f"{r[0]} → {r[1]}%\n"

    send_telegram(msg)
else:
    send_telegram("No stocks in 45% zone today")
