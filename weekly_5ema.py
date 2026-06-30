import yfinance as yf

stock = "RELIANCE.NS"

# Download weekly data
df = yf.download(
    stock,
    period="10y",
    interval="1wk",
    progress=False
)

print(df.tail())
