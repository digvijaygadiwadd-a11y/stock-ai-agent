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

    # Download last 2 years weekly data
    df = yf.download(
        stock,
        period="2y",
        interval="1wk",
        progress=False,
        auto_adjust=False
    )

    if df.empty or len(df) < 6:
        return

    # Flatten MultiIndex if needed
    if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
        df.columns = df.columns.get_level_values(0)

    # 5 EMA
    ema5 = df["Close"].ewm(span=5, adjust=False).mean()

    # Latest COMPLETED weekly candle
    i = len(df) - 2

    open_price = float(df["Open"].iloc[i])
    high_price = float(df["High"].iloc[i])
    low_price = float(df["Low"].iloc[i])
    close_price = float(df["Close"].iloc[i])
    ema = float(ema5.iloc[i])

    print(
        stock,
        df.index[i].date(),
        "Open =", open_price,
        "High =", high_price,
        "Low =", low_price,
        "Close =", close_price,
        "EMA =", round(ema, 2)
    )

    # Entire candle must be below EMA
    if not (
        open_price < ema
        and high_price < ema
        and low_price < ema
        and close_price < ema
    ):
        return

    entry = high_price
    stop_loss = low_price

    print("=" * 70)
    print("LATEST COMPLETED WEEK")
    print("Stock       :", stock)
    print("Signal Date :", df.index[i].date())
    print("Entry       :", entry)
    print("Stop Loss   :", stop_loss)

    # Download latest daily price
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

    print("Current Price :", current_price)

    # Skip if already crossed
    if current_price >= entry:
        print("ENTRY ALREADY TRIGGERED")
        print("=" * 70)
        return

    print(">>> SAVING THIS STOCK <<<")
    print("=" * 70)

    waiting[stock] = {
        "entry": entry,
        "stop_loss": stop_loss,
        "signal_date": str(df.index[i].date()),
        "status": "WAITING"
    }

    save_waiting(waiting)

    print(f"{stock} -> WAITING SETUP SAVED")
