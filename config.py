import os

class Config:
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID   = os.environ.get("TELEGRAM_CHAT_ID")
    ALPHA_VANTAGE_KEY  = os.environ.get("ALPHA_VANTAGE_KEY")
