import yfinance as yf

stock = "RELIANCE.NS"

print(f"\nDownloading Weekly Data for {stock}\n")

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

# Handle MultiIndex columns returned by yfinance
close = df["Close"]
if hasattr(close, "columns"):
    close = close.iloc[:, 0]

# Calculate 5 EMA
df["EMA5"] = close.ewm(span=5, adjust=False).mean()

print(df[["High", "Low", "Close", "EMA5"]].tail(20))
