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

    signal_high = None
    signal_low = None
    signal_date = None

    waiting_for_breakout = False

    # Ignore the latest incomplete weekly candle
    for i in range(len(df) - 1):

        # New signal replaces old one ONLY if breakout hasn't happened
        if high.iloc[i] < ema5.iloc[i]:

            signal_high = float(high.iloc[i])
            signal_low = float(low.iloc[i])
            signal_date = df.index[i]

            waiting_for_breakout = True
            continue

        if waiting_for_breakout:

            if high.iloc[i] > signal_high:

                print("\n🚀 BUY SIGNAL")
                print("-------------------------")
                print("Signal Date :", signal_date)
                print("Entry       :", signal_high)
                print("Stop Loss   :", signal_low)
                print("Breakout On :", df.index[i])

                return

    if waiting_for_breakout:

        print("\n⏳ Waiting For Breakout")
        print("-------------------------")
        print("Signal Date :", signal_date)
        print("Entry       :", signal_high)
        print("Stop Loss   :", signal_low)

    else:

        print("No Signal")
