import json
import yfinance as yf
from utils.telegram_sender import send_message

WAITING_FILE = "waiting_signals.json"


def load_waiting():
    with open(WAITING_FILE, "r") as f:
        return json.load(f)


waiting = load_waiting()

print(f"Found {len(waiting)} waiting stocks.\n")

for stock, data in waiting.items():

    print(f"Checking {stock}")

    print(f"Entry      : {data['entry']}")
    print(f"Stop Loss  : {data['stop_loss']}")
    print(f"Status     : {data['status']}")
    print("----------------------------")
