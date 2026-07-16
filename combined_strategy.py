from rsi_strategy import RSIStrategy

class CombinedStrategy:
    def __init__(self):
        self.rsi = RSIStrategy()

    def analyze(self, df, symbol: str) -> dict:
        rsi_result   = self.rsi.generate_signal(df)

        score        = 0
        buy_reasons  = []
        sell_reasons = []

        if rsi_result["signal"] in ["BUY", "STRONG_BUY"]:
            score += 1
            buy_reasons.append(rsi_result["reason"])
        elif rsi_result["signal"] in ["SELL", "STRONG_SELL"]:
            score -= 1
            sell_reasons.append(rsi_result["reason"])

        if score >= 1:
            final_signal = "🟢 BUY"
        elif score <= -1:
            final_signal = "🔴 SELL"
        else:
            final_signal = "⚪ HOLD"

        return {
            "symbol"       : symbol,
            "signal"       : final_signal,
            "score"        : score,
            "price"        : rsi_result["price"],
            "rsi"          : rsi_result,
            "buy_reasons"  : buy_reasons,
            "sell_reasons" : sell_reasons
        }
