"""
=========================================================
Weekly 5 EMA Strategy
---------------------------------------------------------
This module scans a single NSE stock and detects a
Weekly 5 EMA breakout.

Strategy Rules
--------------
1. Download 10 years of weekly OHLC data.
2. Calculate the 5-week Exponential Moving Average.
3. Find the latest candle completely below the 5 EMA.
4. Use that candle's High as Entry.
5. Use that candle's Low as Stop Loss.
6. Wait for a future candle to break above Entry.
7. Send Telegram alert only once.
8. Store alerted stocks in alerted.json.

Author : Digvijay Gadiwadd
=========================================================
"""

# =====================================================
# IMPORT LIBRARIES
# =====================================================

import json
import os

import yfinance as yf

from utils.telegram_sender import send_message

# =====================================================
# ALERT STORAGE FILE
# =====================================================

ALERT_FILE = "alerted.json"

# =====================================================
# LOAD PREVIOUS ALERTS
# =====================================================


def load_alerts():
    """
    Load all previously alerted stocks.

    This prevents duplicate Telegram notifications
    for the same breakout.
    """

    if os.path.exists(ALERT_FILE):
        try:
            with open(ALERT_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    return {}

# =====================================================
# SAVE ALERT HISTORY
# =====================================================


def save_alerts(alerts):
    """
    Save alerted stocks to JSON file.
    """

    with open(ALERT_FILE, "w") as f:
        json.dump(alerts, f, indent=4)

# =====================================================
# MAIN STRATEGY
# =====================================================


def find_signal(stock):

    alerts = load_alerts()

    try:

        # -------------------------------------------------
        # Download 10 years of weekly historical data
        # -------------------------------------------------

        df = yf.download(
            stock,
            period="10y",
            interval="1wk",
            progress=False,
            auto_adjust=False
        )

        if df.empty:
            return

        # -------------------------------------------------
        # Extract OHLC columns
        # -------------------------------------------------

        high = df["High"]
        low = df["Low"]
        close = df["Close"]

        # Handle MultiIndex columns returned by yfinance

        if hasattr(high, "columns"):
            high = high.iloc[:, 0]

        if hasattr(low, "columns"):
            low = low.iloc[:, 0]

        if hasattr(close, "columns"):
            close = close.iloc[:, 0]

        # -------------------------------------------------
        # Calculate 5-week Exponential Moving Average
        # -------------------------------------------------

        ema5 = close.ewm(span=5, adjust=False).mean()

        # -------------------------------------------------
        # Variables storing the latest valid setup
        # -------------------------------------------------

        signal_high = None
        signal_low = None
        signal_date = None

        # -------------------------------------------------
        # Ignore the current unfinished weekly candle
        # -------------------------------------------------

        for i in range(len(df) - 1):

            # ---------------------------------------------
            # Find latest candle below 5 EMA
            #
            # Entry  = Candle High
            # Stop   = Candle Low
            # ---------------------------------------------

            if high.iloc[i] < ema5.iloc[i]:

                signal_high = float(high.iloc[i])
                signal_low = float(low.iloc[i])
                signal_date = str(df.index[i].date())

            # ---------------------------------------------
            # Breakout Confirmation
            #
            # Breakout occurs when a future candle
            # trades above the stored Entry price.
            # ---------------------------------------------

            elif signal_high is not None:

                if high.iloc[i] > signal_high:

                    # -------------------------------------
                    # Avoid duplicate Telegram alerts
                    # -------------------------------------

                    if stock not in alerts:

                        message = f"""
🚀 WEEKLY 5 EMA BREAKOUT

Stock : {stock}

Entry : ₹{signal_high:.2f}

Stop Loss : ₹{signal_low:.2f}

Signal Date : {signal_date}

Breakout Date : {str(df.index[i].date())}
"""

                        print(message)

                        # Send Telegram notification
                        send_message(message)

                        # Save alert history
                        alerts[stock] = {
                            "signal_date": signal_date,
                            "entry": signal_high,
                            "stop_loss": signal_low,
                            "breakout_date": str(df.index[i].date())
                        }

                        save_alerts(alerts)

                    # Breakout found.
                    # No need to continue scanning.

                    return

    except Exception as e:

        # Continue scanning remaining stocks
        print(f"{stock} FAILED : {e}")
