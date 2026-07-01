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

    yesterday = float(close.iloc[-2])
    today = float(close.iloc[-1])

    entry = data["entry"]
    stop = data["stop_loss"]

    print(
        f"{stock} | Yesterday={yesterday} | Today={today} | Entry={entry}"
    )

    # -----------------------------
    # FAILED
    # -----------------------------
    if today <= stop:

        send_message(
f"""❌ SETUP FAILED

Stock : {stock}

Current Price : ₹{today}

Stop Loss : ₹{stop}
"""
        )

        data["status"] = "FAILED"
        changed = True
        continue

    # -----------------------------
    # TRUE BREAKOUT
    # -----------------------------
    if yesterday < entry and today >= entry:

        send_message(
f"""🚀 BUY SIGNAL

Stock : {stock}

Entry : ₹{entry}

Current Price : ₹{today}

Stop Loss : ₹{stop}
"""
        )

        data["status"] = "BOUGHT"
        changed = True

        print(f"BUY -> {stock}")

if changed:
    save_waiting(waiting)

print("Breakout Monitor Completed")
