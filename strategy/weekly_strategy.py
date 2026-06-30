import yfinance as yf
import json
import os
from utils.telegram_sender import send_message

ALERT_FILE = "alerted.json"


def load_alerts():
    if os.path.exists(ALERT_FILE):
        try:
            with open(ALERT_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_alerts(alerts):
    with open(ALERT_FILE, "w") as f:
        json.dump(alerts, f, indent=4)


def find_signal(stock):

    alerts = load_alerts()

    try:
        df = yf.download(
            stock,
            period="10y",
            interval="1wk",
            progress=False,
            auto_adjust=False,
        )

        if df.empty:
            return

        high = df["High"]
        low = df["Low"]
        close = df["Close"]

        if hasattr(high, "columns"):
            high = high.iloc[:, 0]

        if hasattr(low, "columns"):
            low = low.iloc[:, 0]

        if hasattr(close, "columns"):
            close = close.iloc[:, 0]

        ema5 = close.ewm(span=5, adjust=False).mean()

        signal_high = None
        signal_low = None
        signal_date = None

        # Ignore current unfinished week
        for i in range(len(df) - 1):

            # New signal replaces old signal
            if high.iloc[i] < ema5.iloc[i]:

                signal_high = float(high.iloc[i])
                signal_low = float(low.iloc[i])
                signal_date = str(df.index[i].date())

            # Check breakout
            elif signal_high is not None:

                if high.iloc[i] > signal_high:

                    if stock not in alerts:

                        message = f"""
🚀 WEEKLY 5 EMA BREAKOUT

Stock : {stock}

Entry : ₹{signal_high}

Stop Loss : ₹{signal_low}

Signal Date : {signal_date}

Breakout Date : {str(df.index[i].date())}
"""

print(message)

send_message(message)

                        alerts[stock] = {
                            "signal_date": signal_date,
                            "entry": signal_high,
                            "stop_loss": signal_low,
                            "breakout_date": str(df.index[i].date())
                        }

                        save_alerts(alerts)

                    return

    except Exception:
        print(f"Failed : {stock}")
