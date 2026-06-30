from strategy.weekly_strategy import find_signal

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS"
]

for stock in stocks:
    find_signal(stock)
