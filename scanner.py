import yfinance as yf
import requests

BOT_TOKEN = "8729984501:AAGxp-9ceA4tBGVPm0fHAr--bgkzTbke8zA"
CHAT_ID = "499306024"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

from nselib import capital_market

eq = capital_market.equity_list()
symbols = (eq["SYMBOL"] + ".NS").tolist()

results = []

for stock in symbols:
    try:
        df = yf.download(stock, period="max", progress=False)

        if df.empty:
            continue

        high = df["High"]
        close = df["Close"]

        if hasattr(high, "columns"):
            high = high.iloc[:, 0]

        if hasattr(close, "columns"):
            close = close.iloc[:, 0]

        ath = float(high.max())
        current = float(close.iloc[-1])

        down = ((ath - current) / ath) * 100
        
        ticker = yf.Ticker(stock)
info = ticker.info
market_cap = info.get("marketCap", 0) / 10000000  # ₹ Crore

        if 44 <= down <= 46 and market_cap >= 5000:
            results.append(
    f"📈 {stock}\n"
    f"⬇️ Down from ATH: {down:.2f}%\n"
    f"💰 Market Cap: ₹{market_cap:,.0f} Cr\n"
)

    except Exception as e:
        print(f"Error in {stock}: {e}")

if results:
    message = (
        "🚀 45% ATH STRATEGY ALERT 🚀\n\n"
        + "\n".join(results)
        + f"\n\nTotal Stocks Found: {len(results)}"
    )
else:
    message = "❌ No stocks near the 45% ATH zone today."

send_telegram(message)
print(message)
