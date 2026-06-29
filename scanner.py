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

    ath = float(df["High"].max())
    current = float(df["Close"].iloc[-1])

    down = float(((ath - current) / ath) * 100)

    if 44 <= down <= 46:
        print(stock, down)
