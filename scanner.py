import json
import requests
import yfinance as yf
from nselib import capital_market
from datetime import datetime

BOT_TOKEN = "8729984501:AAGxp-9ceA4tBGVPm0fHAr--bgkzTbke8zA"
CHAT_ID = "499306024"


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


print(f"Scan started at {datetime.now()}")

# Scan ALL NSE stocks
eq = capital_market.equity_list()
symbols = (eq["SYMBOL"] + ".NS").tolist()

results = []

# Load previously alerted stocks
try:
    with open("alerted.json", "r") as f:
        alerted = set(json.load(f))
except:
    alerted = set()

new_alerted = set()

for stock in symbols:
    try:
        df = yf.download(
            stock,
            period="max",
            progress=False,
            auto_adjust=False
        )

        if df.empty:
            continue

        high = df["High"]
        close = df["Close"]

        # Handle MultiIndex columns if returned
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

        if (
            44 <= down <= 46
            and market_cap >= 5000
            and stock not in alerted
        ):
            results.append(
                f"📈 {stock}\n"
                f"⬇️ Down from ATH: {down:.2f}%\n"
                f"💰 Market Cap: ₹{market_cap:,.0f} Cr\n"
            )

            new_alerted.add(stock)

    except Exception as e:
        print(f"Error in {stock}: {e}")

today = datetime.now().strftime("%d-%b-%Y")

if results:
    message = (
        f"🚀 45% ATH STRATEGY ALERT 🚀\n"
        f"📅 {today}\n\n"
        + "\n".join(results)
        + f"\n\nTotal Stocks Found: {len(results)}"
    )
else:
    message = (
        f"📅 {today}\n"
        "❌ No stocks near the 45% ATH zone today."
    )

# Save alerted stocks
with open("alerted.json", "w") as f:
    json.dump(sorted(alerted | new_alerted), f)

send_telegram(message)
print(message)

print(f"Scan finished at {datetime.now()}")
