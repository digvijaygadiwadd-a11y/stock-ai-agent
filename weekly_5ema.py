import yfinance as yf

stock = "RELIANCE.NS"

print("Downloading Weekly Data...\n")

df = yf.download(
    stock,
    period="10y",
    interval="1wk",
    progress=False,
    auto_adjust=False
)

if df.empty:
    print("No data found.")
else:
    print(df.tail(15))
