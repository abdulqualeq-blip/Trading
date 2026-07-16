import yfinance as yf
import pandas as pd

class YahooFinanceAPI:

    def get_data(
        self,
        symbol  : str,
        period  : str = "3mo",
        interval: str = "1d"
    ) -> pd.DataFrame:
        ticker = yf.Ticker(symbol)
        df     = ticker.history(period=period, interval=interval)
        df.columns = df.columns.str.lower()
        return df

    def get_india_data(
        self,
        symbol  : str,
        period  : str = "3mo",
        interval: str = "1d"
    ) -> pd.DataFrame:
        # NSE stocks need .NS at the end
        nse_symbol = f"{symbol}.NS"
        return self.get_data(nse_symbol, period=period, interval=interval)
