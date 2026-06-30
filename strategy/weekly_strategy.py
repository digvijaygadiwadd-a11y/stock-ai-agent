import yfinance as yf


def find_signal(stock):

    print(f"\nScanning {stock}")

    df = yf.download(
        stock,
        period="10y",
        interval="1wk",
        progress=False,
        auto_adjust=False
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

    signal_index = None

    for i in range(len(df)):

        if high.iloc[i] < ema5.iloc[i]:

            signal_index = i

    if signal_index is None:
        print("No Signal")
        return

    signal_high = float(high.iloc[signal_index])
    signal_low = float(low.iloc[signal_index])

    print("Signal Found")
    print("High :", signal_high)
    print("Low  :", signal_low)

    for i in range(signal_index + 1, len(df)):

        if high.iloc[i] > signal_high:

            print("🚀 BUY SIGNAL")
            print("Entry :", signal_high)
            print("Stop :", signal_low)
            return

    print("Waiting For Breakout")
