import yfinance as yf


def find_signal(stock):

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

    signal_high = None
    signal_low = None

    for i in range(len(df) - 1):

        if high.iloc[i] < ema5.iloc[i]:

            signal_high = float(high.iloc[i])
            signal_low = float(low.iloc[i])

        elif signal_high is not None:

            if high.iloc[i] > signal_high:

                print("===================================")
                print(stock)
                print("BUY SIGNAL")
                print("Entry :", signal_high)
                print("SL :", signal_low)
                print("===================================")

                return
