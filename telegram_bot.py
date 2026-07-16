import os

class Config:
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID")
    ALPHA_VANTAGE_KEY  = os.environ.get("ALPHA_VANTAGE_KEY")
import requests
from config import Config

class TelegramBot:
    def __init__(self):
        self.token    = Config.TELEGRAM_BOT_TOKEN
        self.chat_id  = Config.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, message: str) -> bool:
        url     = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id"    : self.chat_id,
            "text"       : message,
            "parse_mode" : "HTML"
        }
        try:
            response = requests.post(url, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"Telegram Error: {e}")
            return False

    def send_alert(self, analysis: dict, market: str = "US") -> bool:
        flag   = "🇺🇸" if market == "US" else "🇮🇳"
        signal = analysis['signal']
        symbol = analysis['symbol']
        price  = analysis['price']
        rsi    = analysis['rsi']['rsi']

        buy_text  = "\n".join(f"✅ {r}" for r in analysis['buy_reasons'])  or "None"
        sell_text = "\n".join(f"❌ {r}" for r in analysis['sell_reasons']) or "None"

        message = f"""{flag} <b>TRADING ALERT</b>

📌 Stock  : <b>{symbol}</b>
📊 Signal : <b>{signal}</b>
💰 Price  : <b>{price}</b>
📈 RSI    : <b>{rsi}</b>

<b>Buy Reasons:</b>
{buy_text}

<b>Sell Reasons:</b>
{sell_text}"""

        return self.send_message(message)
