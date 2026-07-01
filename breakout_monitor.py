import json
import os
import yfinance as yf
from utils.telegram_sender import send_message

WAITING_FILE = "waiting_signals.json"
HISTORY_FILE = "trade_history.json"


def load_json(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)
    return {}


def save_json(file_name, data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)


waiting = load_json(WAITING_FILE)
history = load_json(HISTORY_FILE)

print(f"Found {len(waiting)} waiting stocks.\n")

completed = []

for stock, data in waiting.items():

    if data["status"] != "WAITING":
        continue

    df = yf.download(
        stock,
        period="10d",
        interval="1d",
        progress=False,
        auto_adjust=False
    )

    if df.empty or len(df) < 2:
        continue

    if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
        df.columns = df.columns.get_level_values(0)

    close = df["Close"]
    low = df["Low"]

    if hasattr(close, "columns"):
        close = close.iloc[:, 0]

    if hasattr(low, "columns"):
        low = low.iloc[:, 0]

    yesterday_close = float(close.iloc[-2])
    current_price = float(close.iloc[-1])
    today_low = float(low.iloc[-1])

    entry = float(data["entry"])
    stop = float(data["stop_loss"])

    print(
        f"{stock} | "
        f"Yesterday={yesterday_close} | "
        f"CMP={current_price} | "
        f"Low={today_low} | "
        f"Entry={entry} | "
        f"SL={stop}"
    )

    # ===========================
    # FAILED
    # ===========================

    if today_low <= stop:

        message = f"""
❌ SETUP FAILED

Stock : {stock}

Entry : ₹{entry}

CMP : ₹{current_price}

Stop Loss : ₹{stop}
"""

        send_message(message)

        data["status"] = "FAILED"
        data["exit_price"] = current_price

        history[stock] = data

        completed.append(stock)

        print(f"FAILED -> {stock}")

        continue

    # ===========================
    # BUY
    # ===========================

    if yesterday_close < entry and current_price >= entry:

        message = f"""
🚀 BUY SIGNAL

Stock : {stock}

Entry : ₹{entry}

CMP : ₹{current_price}

Stop Loss : ₹{stop}
"""

        send_message(message)

        data["status"] = "BOUGHT"
        data["buy_price"] = current_price

        history[stock] = data

        completed.append(stock)

        print(f"BUY -> {stock}")

# Remove completed stocks from waiting list
for stock in completed:
    waiting.pop(stock, None)

save_json(WAITING_FILE, waiting)
save_json(HISTORY_FILE, history)

print("\nWaiting Stocks :", len(waiting))
print("Trade History :", len(history))
print("Breakout Monitor Completed")
