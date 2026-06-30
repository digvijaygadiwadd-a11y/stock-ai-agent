import json
import yfinance as yf
from utils.telegram_sender import send_message

WAITING_FILE = "waiting_signals.json"


def load_waiting():
    with open(WAITING_FILE, "r") as f:
        return json.load(f)


def get_latest_price(stock):
    df = yf.download(
        stock,
        period="5d",
        interval="1d",
        progress=False,
        auto_adjust=False
    )

    if df.empty:
        return None

    close = df["Close"]

    if hasattr(close, "columns"):
        close = close.iloc[:, 0]

    return float(close.iloc[-1])


waiting = load_waiting()

print(f"Found {len(waiting)} waiting stocks.\n")

for stock, data in waiting.items():

    print(f"\nChecking {stock}")

    latest_price = get_latest_price(stock)

    if latest_price is None:
        print("Price not available")
        continue

    print(f"Current Price : {latest_price}")
    print(f"Entry         : {data['entry']}")
    print(f"Stop Loss     : {data['stop_loss']}")
    print(f"Status        : {data['status']}")

    if (
        data["status"] == "WAITING"
        and latest_price >= data["entry"]
    ):
        print(f"BUY SIGNAL -> {stock}")
    else:
        print("No Breakout")

    print("----------------------------")
