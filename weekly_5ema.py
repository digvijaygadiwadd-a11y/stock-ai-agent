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

# Handle MultiIndex
high = df["High"]
low = df["Low"]
close = df["Close"]

if hasattr(high, "columns"):
    high = high.iloc[:, 0]

if hasattr(low, "columns"):
    low = low.iloc[:, 0]

if hasattr(close, "columns"):
    close = close.iloc[:, 0]

# Weekly EMA
ema5 = close.ewm(span=5, adjust=False).mean()

# -------------------------------
# Find Latest Signal Candle
# -------------------------------

signal_index = None

for i in range(len(df) - 1):
    if high.iloc[i] < ema5.iloc[i]:
        signal_index = i

if signal_index is None:
    print("❌ No Signal Candle Found")
    exit()

signal_date = df.index[signal_index]
signal_high = float(high.iloc[signal_index])
signal_low = float(low.iloc[signal_index])

print("✅ Latest Signal Candle")
print("----------------------")
print(f"Date : {signal_date}")
print(f"High : {signal_high:.2f}")
print(f"Low  : {signal_low:.2f}")

# -------------------------------
# Check Breakout
# -------------------------------

latest_high = float(high.iloc[-1])
latest_close = float(close.iloc[-1])

print("\nLatest Week")
print("----------------------")
print(f"High  : {latest_high:.2f}")
print(f"Close : {latest_close:.2f}")

if latest_high > signal_high:
    print("\n🚀 BUY SIGNAL GENERATED")
    print(f"Entry : {signal_high:.2f}")
    print(f"Stop Loss : {signal_low:.2f}")
else:
    print("\n⏳ Waiting for Breakout...")
