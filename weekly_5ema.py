from strategy.weekly_strategy import find_signal
from nsepython import nse_eq_symbols

print("Downloading NSE Stock List...")

stocks = nse_eq_symbols()

print(f"Total Stocks : {len(stocks)}")

for stock in stocks:

    symbol = stock + ".NS"

    try:
        find_signal(symbol)

    except Exception as e:
        print(symbol, e)
