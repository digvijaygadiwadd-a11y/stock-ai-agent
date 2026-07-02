"""
=========================================================
Weekly 5 EMA Scanner
---------------------------------------------------------
This script downloads all NSE-listed stocks and scans
each one using the Weekly 5 EMA strategy.

For every stock:
1. Fetch weekly historical data
2. Apply the Weekly 5 EMA strategy
3. Save valid waiting setups

Author: Digvijay Gadiwadd
=========================================================
"""

# ==========================================
# IMPORT REQUIRED LIBRARIES
# ==========================================

from strategy.weekly_strategy import find_signal
from nsepython import nse_eq_symbols

# ==========================================
# DOWNLOAD COMPLETE NSE STOCK LIST
# ==========================================

print("=" * 60)
print("Downloading NSE Stock List...")
print("=" * 60)

stocks = nse_eq_symbols()

print(f"Total NSE Stocks Found : {len(stocks)}")
print()

# ==========================================
# SCAN EVERY NSE STOCK
# ==========================================

for stock in stocks:

    # Convert NSE symbol into Yahoo Finance format
    symbol = stock + ".NS"

    try:

        # --------------------------------------
        # Run Weekly 5 EMA Strategy
        #
        # The strategy will:
        #
        # • Download weekly price data
        # • Calculate 5-week EMA
        # • Check whether the entire candle
        #   is below the EMA
        # • Verify breakout has not happened
        # • Ignore setups older than 8 weeks
        # • Save valid setups to
        #   waiting_signals.json
        # --------------------------------------

        find_signal(symbol)

    except Exception as e:

        # Continue scanning even if one stock fails
        print(f"{symbol} -> {e}")

print()
print("=" * 60)
print("Weekly Scan Completed Successfully")
print("=" * 60)
