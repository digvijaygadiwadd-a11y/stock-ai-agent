from strategy.weekly_setup import find_weekly_setup
from nsepython import nse_eq_symbols

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
