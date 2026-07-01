import json
import os
import yfinance as yf

WAITING_FILE = "waiting_signals.json"


def load_waiting():
    if os.path.exists(WAITING_FILE):
        with open(WAITING_FILE, "r") as f:
            return json.load(f)
    return {}


def save_waiting(data):
    with open(WAITING_FILE, "w") as f:
        json.dump(data, f, indent=4)


def find_weekly_setup(stock):

    waiting = load_waiting()

    # Weekly candles
    weekly = yf.download(
        stock,
        period="2y",
        interval="1wk",
        progress=False,
        auto_adjust=False
    )

    if weekly.empty or len(weekly) < 10:
        return

    # Flatten MultiIndex if needed
    if hasattr(weekly.columns, "nlevels") and weekly.columns.nlevels > 1:
        weekly.columns = weekly.columns.get_level_values(0)

    ema5 = weekly["Close"].ewm(span=5, adjust=False).mean()

    latest_valid_signal = None

    # Ignore current unfinished week
    for i in range(5, len(weekly) - 1):

        open_price = float(weekly["Open"].iloc[i])
        high_price = float(weekly["High"].iloc[i])
        low_price = float(weekly["Low"].iloc[i])
        close_price = float(weekly["Close"].iloc[i])
        ema = float(ema5.iloc[i])

        # Entire candle below EMA
        if not (
            open_price < ema
            and high_price < ema
            and low_price < ema
            and close_price < ema
        ):
            continue

        entry = high_price
        stop_loss = low_price

        # --------------------------------------------------
        # Has breakout already happened in ANY later week?
        # --------------------------------------------------
        breakout = False

        for j in range(i + 1, len(weekly) - 1):

            future_high = float(weekly["High"].iloc[j])

            if future_high >= entry:
                breakout = True
                break

        if breakout:
            continue

        # Keep only the latest valid signal
        latest_valid_signal = {
            "entry": entry,
            "stop_loss": stop_loss,
            "signal_date": str(weekly.index[i].date()),
            "status": "WAITING"
        }

    # No valid waiting setup
    if latest_valid_signal is None:
        return

    # --------------------------------------------------
    # Check today's price
    # --------------------------------------------------

    daily = yf.download(
        stock,
        period="5d",
        interval="1d",
        progress=False,
        auto_adjust=False
    )

    if daily.empty:
        return

    if hasattr(daily.columns, "nlevels") and daily.columns.nlevels > 1:
        daily.columns = daily.columns.get_level_values(0)

    current_price = float(daily["Close"].iloc[-1])

    # Today's price already crossed entry
    if current_price >= latest_valid_signal["entry"]:
        print(f"{stock} -> ENTRY ALREADY TRIGGERED")
        return

    waiting[stock] = latest_valid_signal

    save_waiting(waiting)

    print(
        f"{stock} -> WAITING SETUP SAVED | "
        f"Date={latest_valid_signal['signal_date']} | "
        f"Entry={latest_valid_signal['entry']} | "
        f"Current={current_price}"
    )
