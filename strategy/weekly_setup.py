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

    df = yf.download(
        stock,
        period="10y",
        interval="1wk",
        progress=False,
        auto_adjust=False
    )

    if df.empty:
        return

    # Flatten columns if yfinance returns MultiIndex
    if hasattr(df.columns, "nlevels") and df.columns.nlevels > 1:
        df.columns = df.columns.get_level_values(0)

    ema5 = df["Close"].ewm(span=5, adjust=False).mean()

    latest_signal = None

    #     # Ignore the current unfinished weekly candle
    for i in range(len(df) - 1):

        print(
            stock,
            df.index[i].date(),
            "Open =", float(df["Open"].iloc[i]),
            "High =", float(df["High"].iloc[i]),
            "Low =", float(df["Low"].iloc[i]),
            "Close =", float(df["Close"].iloc[i]),
            "EMA =", round(float(ema5.iloc[i]), 2)
        )

        # Entire candle must be below EMA
        if (
            df["Open"].iloc[i] < ema5.iloc[i]
            and df["High"].iloc[i] < ema5.iloc[i]
            and df["Low"].iloc[i] < ema5.iloc[i]
            and df["Close"].iloc[i] < ema5.iloc[i]
        ):

            print("VALID SIGNAL FOUND:", stock, df.index[i].date())

            latest_signal = {
                "entry": float(df["High"].iloc[i]),
                "stop_loss": float(df["Low"].iloc[i]),
                "signal_date": str(df.index[i].date()),
                "status": "WAITING"
            }

    if latest_signal is not None:

        waiting[stock] = latest_signal
        save_waiting(waiting)

        print(f"{stock} -> Setup Saved")Ignore the current unfinished weekly candle
     # for i in range(len(df) - 1):

    
