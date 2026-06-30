import json
import yfinance as yf
from utils.telegram_sender import send_message

WAITING_FILE = "waiting_signals.json"


def load_waiting():
    try:
        with open(WAITING_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


waiting = load_waiting()

print(f"Total Waiting Stocks : {len(waiting)}")
