import json

from strategy.weekly_setup import find_weekly_setup
from nsepython import nse_eq_symbols

# Start every weekly scan with a fresh watchlist
with open("waiting_signals.json", "w") as f:
    json.dump({}, f, indent=4)

print("Downloading NSE Stock List...")

stocks = nse_eq_symbols()

print(f"Total Stocks : {len(stocks)}")

for stock in stocks:

    symbol = stock + ".NS"

    try:
        find_weekly_setup(symbol)

    except Exception as e:
        print(symbol, e)

print("Weekly Setup Scan Completed")
