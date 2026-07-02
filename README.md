# 📈 AI-Powered NSE Stock Scanner

An automated stock scanning system that identifies high-probability swing trading opportunities in NSE stocks using a custom 5 EMA strategy.

The project automatically scans stocks, tracks waiting setups, monitors breakouts, and sends Telegram alerts using GitHub Actions.

---

# 🚀 Features

✅ Weekly scan of all NSE stocks

✅ Detects Weekly 5 EMA setup

✅ Stores waiting breakout candidates

✅ Daily Watchlist generation

✅ Automatic Breakout Monitoring

✅ Telegram Buy Alerts

✅ Telegram Failed Setup Alerts

✅ Fully automated using GitHub Actions

---

# 📊 Strategy

The scanner searches for stocks where:

- Entire weekly candle is below 5 EMA
- No breakout has happened after the setup candle
- Setup is not older than 8 weeks
- Entry = High of setup candle
- Stop Loss = Low of setup candle

When price crosses the Entry level:

→ 🚀 BUY SIGNAL

If price breaks below Stop Loss before breakout:

→ ❌ SETUP FAILED

---

# ⚙️ Automation

## Weekly Setup Scanner

Runs every Saturday.

- Scans all NSE stocks
- Finds fresh setups
- Saves them in `waiting_signals.json`

---

## Daily Watchlist

Runs every weekday morning.

Generates today's watchlist and sends it to Telegram.

Example:

```
⭐ DAILY WATCHLIST ⭐

Total Waiting Stocks : 137

ABMINTLLTD.NS

CMP : ₹41.90

Entry : ₹43.22
```

---

## Breakout Monitor

Runs every weekday.

Checks all waiting stocks.

If breakout occurs:

```
🚀 BUY SIGNAL

Stock : ABCXYZ.NS

Entry : ₹425

CMP : ₹428

Stop Loss : ₹398
```

If setup fails:

```
❌ SETUP FAILED

Stock : ABCXYZ.NS

Entry : ₹425

CMP : ₹392

Stop Loss : ₹398
```

---

# 🛠 Tech Stack

- Python
- GitHub Actions
- yfinance
- NSELib
- Telegram Bot API
- JSON
- Requests

---

# 📂 Project Structure

```
.
├── .github/
│   └── workflows/
│       ├── daily_watchlist.yml
│       ├── breakout_monitor.yml
│       ├── weekly_5ema.yml
│
├── strategy/
│
├── utils/
│   └── telegram_sender.py
│
├── weekly_5ema.py
├── breakout_monitor.py
├── daily_watchlist.py
├── scanner.py
│
├── waiting_signals.json
├── trade_history.json
├── alerted.json
│
└── README.md
```

---

# ▶️ Running Locally

Install dependencies

```bash
pip install -r requirements.txt
```

Run Weekly Scanner

```bash
python weekly_5ema.py
```

Run Daily Watchlist

```bash
python daily_watchlist.py
```

Run Breakout Monitor

```bash
python breakout_monitor.py
```

---

# 📱 Telegram Notifications

The project automatically sends:

- Daily Watchlist
- Buy Signals
- Failed Setup Alerts

using the Telegram Bot API.

---

# 📸 Sample Output

## Daily Watchlist

```
⭐ DAILY WATCHLIST ⭐

Total Waiting Stocks : 137

ABCOTS.NS

CMP : ₹220.56

Entry : ₹299.00
```

---

## Buy Signal

```
🚀 BUY SIGNAL

Stock : XYZ.NS

Entry : ₹452

CMP : ₹455

Stop Loss : ₹430
```

---

## Failed Setup

```
❌ SETUP FAILED

Stock : XYZ.NS

Entry : ₹452

CMP : ₹428

Stop Loss : ₹430
```

---

# 👨‍💻 Author

**Digvijay Gadiwadd**

Civil Engineer | Aspiring Business Analyst | AI Automation Enthusiast

LinkedIn:
(Add your LinkedIn profile URL here)

GitHub:
https://github.com/digvijaygadiwadd-a11y

---

# ⭐ Future Improvements

- Portfolio Dashboard
- Trade Performance Analytics
- Volume Confirmation
- Relative Strength Ranking
- Position Sizing Calculator
- Web Dashboard
- Database Integration
