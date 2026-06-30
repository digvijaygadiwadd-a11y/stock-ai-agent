import yfinance as yf

stock = "RELIANCE.NS"

print(f"\nScanning {stock}...\n")

# Download weekly data
df = yf.download(
    stock,
    period="10y",
    interval="1wk",
    progress=False,
    auto_adjust=False
)

if df.empty:
    print("No data found.")
    exit()

# Handle MultiIndex columns
high = df["High"]
low = df["Low"]
close = df["Close"]

if hasattr(high, "columns"):
    high = high.iloc[:, 0]

if hasattr(low, "columns"):
    low = low.iloc[:, 0]

if hasattr(close, "columns"):
    close = close.iloc[:, 0]

# Calculate Weekly 5 EMA
ema5 = close.ewm(span=5, adjust=False).mean()

# Find the latest signal candle
signal_found = False

for i in range(len(df)):
    if high.iloc[i] < ema5.iloc[i]:
        signal_found = True

        signal_date = df.index[i]
        signal_high = float(high.iloc[i])
        signal_low = float(low.iloc[i])

if signal_found:
    print("✅ Latest Signal Found\n")
    print(f"Date : {signal_date}")
    print(f"High : {signal_high}")
    print(f"Low  : {signal_low}")
else:
    print("❌ No Signal Found")
