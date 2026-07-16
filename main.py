import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from yahoo_finance import YahooFinanceAPI
from telegram_bot import TelegramBot
from combined_strategy import CombinedStrategy

app = FastAPI(title="Trading Alert System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

yahoo    = YahooFinanceAPI()
telegram = TelegramBot()
strategy = CombinedStrategy()

# ─────────────────────────────────────────
@app.get("/")
def home():
    return {"message": "Trading Alert System Running ✅"}

# ─────────────────────────────────────────
@app.get("/analyze/{symbol}")
def analyze(symbol: str, market: str = "US"):
    try:
        df     = yahoo.get_india_data(symbol) if market == "INDIA" else yahoo.get_data(symbol)
        result = strategy.analyze(df, symbol)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ─────────────────────────────────────────
@app.get("/alert/{symbol}")
def send_alert(symbol: str, market: str = "US"):
    try:
        df     = yahoo.get_india_data(symbol) if market == "INDIA" else yahoo.get_data(symbol)
        result = strategy.analyze(df, symbol)
        telegram.send_alert(result, market)
        return {"message": f"Alert sent for {symbol}!", "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ─────────────────────────────────────────
@app.get("/scan")
def scan_stocks(market: str = "US"):
    us_stocks    = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
    india_stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "WIPRO"]
    stocks       = us_stocks if market == "US" else india_stocks
    results      = []

    for symbol in stocks:
        try:
            df     = yahoo.get_india_data(symbol) if market == "INDIA" else yahoo.get_data(symbol)
            result = strategy.analyze(df, symbol)
            results.append(result)
            if abs(result["score"]) >= 1:
                telegram.send_alert(result, market)
        except Exception as e:
            print(f"Error {symbol}: {e}")

    return {"scanned": len(results), "results": results}

# ─────────────────────────────────────────
@app.get("/test-telegram")
def test_telegram():
    success = telegram.send_message("✅ <b>Trading Bot is Live!</b>")
    return {"telegram_working": success}

