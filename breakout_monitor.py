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


waiting = load_waiting()

changed = False

print(f"Found {len(waiting)} waiting stocks.\n")

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

    # ==========================
    # FAILED
    # ==========================

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

        changed = True

        print(f"FAILED -> {stock}")

        continue

    # ==========================
    # TRUE BREAKOUT
    # ==========================

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

        changed = True

        print(f"BUY -> {stock}")

if changed:
    save_waiting(waiting)

print("\nBreakout Monitor Completed")
