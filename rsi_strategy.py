import pandas as pd

class RSIStrategy:
    def __init__(self, period=14, oversold=30, overbought=70):
        self.period     = period
        self.oversold   = oversold
        self.overbought = overbought

    def calculate_rsi(self, df: pd.DataFrame) -> pd.Series:
        delta = df["close"].diff()
        gain  = delta.where(delta > 0, 0).rolling(self.period).mean()
        loss  = (-delta.where(delta < 0, 0)).rolling(self.period).mean()
        rs    = gain / loss
        return 100 - (100 / (1 + rs))

    def generate_signal(self, df: pd.DataFrame) -> dict:
        df         = df.copy()
        df["rsi"]  = self.calculate_rsi(df)

        latest_rsi = df["rsi"].iloc[-1]
        prev_rsi   = df["rsi"].iloc[-2]
        price      = df["close"].iloc[-1]

        signal = "HOLD"
        reason = ""

        if prev_rsi < self.oversold and latest_rsi >= self.oversold:
            signal = "BUY"
            reason = "RSI crossed above oversold zone"
        elif prev_rsi > self.overbought and latest_rsi <= self.overbought:
            signal = "SELL"
            reason = "RSI crossed below overbought zone"
        elif latest_rsi < self.oversold:
            signal = "STRONG_BUY"
            reason = f"RSI very oversold at {latest_rsi:.1f}"
        elif latest_rsi > self.overbought:
            signal = "STRONG_SELL"
            reason = f"RSI very overbought at {latest_rsi:.1f}"

        return {
            "signal" : signal,
            "reason" : reason,
            "rsi"    : round(latest_rsi, 2),
            "price"  : round(price, 2)
        }
