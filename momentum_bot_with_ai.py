import pandas as pd
from bot import MomentumBot
from ai_model import AIModel


class MomentumBotWithAI(MomentumBot):
    def __init__(self, initial_balance=10000, ai_model_path="ai_model.pkl"):
        super().__init__(initial_balance=initial_balance)
        self.ai = AIModel(model_path=ai_model_path)
        try:
            self.ai.load()
            print(f"🤖 AI model loaded from {ai_model_path}")
        except Exception as e:
            print(f"⚠️ Could not load AI model: {e}")

    def momentum_strategy_with_ai(self, price_history, high_prices, low_prices, close_prices, volume_data=None):
        """
        Extend momentum strategy by combining technical consensus with AI prediction.
        """
        # Step 1: Run the original momentum strategy
        base_result = super().momentum_strategy(price_history, high_prices, low_prices, close_prices, volume_data)

        if not base_result or not isinstance(base_result, dict):
            return base_result

        # Step 2: Prepare AI features (example using indicators from result)
        features = [
            base_result["ema_13"] or 0,
            base_result["ema_20"] or 0,
            base_result["ema_50"] or 0,
            base_result["stoch_k"] or 0,
            base_result["stoch_d"] or 0,
            base_result["ao_current"] or 0
        ]

        # Step 3: AI prediction (1 = BUY, -1 = SELL, 0 = HOLD)
        try:
            ai_signal = self.ai.predict(features)
        except Exception as e:
            print(f"⚠️ AI prediction failed: {e}")
            ai_signal = 0

        # Step 4: Combine signals
        final_buy = base_result["buy_signal"] or (ai_signal == 1)
        final_sell = base_result["sell_signal"] or (ai_signal == -1)

        # Step 5: Add AI decision to the result
        base_result["ai_signal"] = ai_signal
        base_result["final_buy_signal"] = final_buy
        base_result["final_sell_signal"] = final_sell

        if ai_signal == 1:
            base_result["signals"].append("AI: BUY")
        elif ai_signal == -1:
            base_result["signals"].append("AI: SELL")
        else:
            base_result["signals"].append("AI: HOLD")

        return base_result


# Example usage
if __name__ == "__main__":
    bot = MomentumBotWithAI(initial_balance=10000)

    # Load CSV created by data.py
    df = pd.read_csv("your_data.csv")
    prices = df["Close"].tolist()
    highs = df["High"].tolist() if "High" in df.columns else prices
    lows = df["Low"].tolist() if "Low" in df.columns else prices

    result = bot.momentum_strategy_with_ai(
        price_history=prices[-60:],  # last 60 candles
        high_prices=highs[-60:],
        low_prices=lows[-60:],
        close_prices=prices[-60:]
    )

    print("📊 Final Strategy Output with AI:")
    print(result)
