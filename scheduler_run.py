import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from apis.yahoo_finance import YahooFinanceAPI
from apis.telegram_bot  import TelegramBot
from strategies.combined_strategy import CombinedStrategy
from datetime import datetime
import pytz

yahoo    = YahooFinanceAPI()
telegram = TelegramBot()
strategy = CombinedStrategy()

US_STOCKS    = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
INDIA_STOCKS = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "WIPRO"]

def scan_and_alert(stocks, market):
    for symbol in stocks:
        try:
            df     = yahoo.get_india_data(symbol) if market == "INDIA" else yahoo.get_data(symbol)
            result = strategy.analyze(df, symbol)
            if abs(result["score"]) >= 1:
                telegram.send_alert(result, market)
                print(f"✅ Alert: {symbol} → {result['signal']}")
            else:
                print(f"⚪ Hold : {symbol}")
        except Exception as e:
            print(f"❌ Error {symbol}: {e}")

if __name__ == "__main__":
    ist     = pytz.timezone("Asia/Kolkata")
    est     = pytz.timezone("America/New_York")
    now_ist = datetime.now(ist)
    now_est = datetime.now(est)

    print(f"🕒 Running at {now_ist.strftime('%H:%M')} IST")

    if 9 <= now_ist.hour <= 15 and now_ist.weekday() < 5:
        print("🇮🇳 Scanning India...")
        scan_and_alert(INDIA_STOCKS, "INDIA")

    if 9 <= now_est.hour <= 16 and now_est.weekday() < 5:
        print("🇺🇸 Scanning US...")
        scan_and_alert(US_STOCKS, "US")
