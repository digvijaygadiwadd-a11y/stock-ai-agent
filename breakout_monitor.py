import json
import yfinance as yf
from utils.telegram_sender import send_message

WAITING_FILE = "waiting_signals.json"


def load_waiting():
    with open(WAITING_FILE, "r") as f:
        return json.load(f)


def save_waiting(data):
    with open(WAITING_FILE, "w") as f:
        json.dump(data, f, indent=4)


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

print(f"Found {len(waiting)} waiting stocks.")

changed = False

for stock, data in waiting.items():

    latest_price = get_latest_price(stock)

    if latest_price is None:
        continue

    print(
        f"{stock} | Current={latest_price} | "
        f"Entry={data['entry']} | "
        f"SL={data['stop_loss']} | "
        f"Status={data['status']}"
    )

    # Skip completed setups
    if data["status"] != "WAITING":
        continue

    # FAILED
    if latest_price <= data["stop_loss"]:

        message = f"""
❌ SETUP FAILED

Stock : {stock}

Current Price : ₹{latest_price}

Stop Loss : ₹{data['stop_loss']}
"""

        send_message(message)

        data["status"] = "FAILED"

        changed = True

        print(f"FAILED -> {stock}")

        continue

    # BUY
    if latest_price >= data["entry"]:

        message = f"""
🚀 BUY SIGNAL

Stock : {stock}

Entry : ₹{data['entry']}

Current Price : ₹{latest_price}

Stop Loss : ₹{data['stop_loss']}
"""

        send_message(message)

        data["status"] = "BOUGHT"

        changed = True

        print(f"BUY -> {stock}")

if changed:

    save_waiting(waiting)

    print("waiting_signals.json updated.")
