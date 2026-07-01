import json
import os
import yfinance as yf
from utils.telegram_sender import send_message

WAITING_FILE = "waiting_signals.json"


if not os.path.exists(WAITING_FILE):
    print("No waiting file found.")
    exit()

with open(WAITING_FILE, "r") as f:
    waiting = json.load(f)

watchlist = []

for stock, data in waiting.items():

    if data["status"] != "WAITING":
        continue

    df = yf.download(
        stock,
        period="5d",
        interval="1d",
        progress=False,
        auto_adjust=False
    )

    if df.empty:
        continue

    if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
        df.columns = df.columns.get_level_values(0)

    close = df["Close"]

    if hasattr(close, "columns"):
        close = close.iloc[:, 0]

    cmp = float(close.iloc[-1])

    entry = float(data["entry"])

    distance = ((entry - cmp) / entry) * 100

    if distance < 0:
        continue

    watchlist.append({
        "stock": stock,
        "cmp": cmp,
        "entry": entry,
        "distance": distance
    })

watchlist.sort(key=lambda x: x["distance"])

message = "📊 DAILY BREAKOUT WATCHLIST\n\n"

message += f"Waiting Stocks : {len(watchlist)}\n\n"

for i, s in enumerate(watchlist[:20], start=1):

    message += (
        f"{i}. {s['stock']}\n"
        f"CMP : ₹{s['cmp']:.2f}\n"
        f"Entry : ₹{s['entry']:.2f}\n"
        f"Distance : {s['distance']:.2f}%\n\n"
    )

send_message(message)

print("Watchlist Sent")
