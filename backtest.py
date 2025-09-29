import pandas as pd
from bot import MomentumBot  # make sure bot.py has your MomentumBot class

class Backtester:
    def __init__(self, initial_balance: float = 10000.0):
        self.initial_balance = initial_balance
        self.bot = MomentumBot(initial_balance=initial_balance)

    def run_backtest(self, csv_path: str):
        df = pd.read_csv(csv_path)

        trades = []
        equity_curve = [self.initial_balance]

        for i in range(len(df)):
            price = df.loc[i, "Close"]
            high = df.loc[i, "High"] if "High" in df.columns else price
            low = df.loc[i, "Low"] if "Low" in df.columns else price

            # run strategy on history up to this point
            result = self.bot.momentum_strategy(
                price_history=df["Close"].iloc[: i + 1].tolist(),
                high_prices=df["High"].iloc[: i + 1].tolist() if "High" in df.columns else [],
                low_prices=df["Low"].iloc[: i + 1].tolist() if "Low" in df.columns else [],
                close_prices=df["Close"].iloc[: i + 1].tolist(),
            )

            if not result:
                equity_curve.append(self.bot.account_balance)
                continue

            # open trade
            if result["buy_signal"] and not self.bot.in_position:
                self.bot.execute_trade(
                    "BUY", price, result["position_size"],
                    result["stop_loss"], result["take_profit"]
                )
                trades.append({"type": "BUY", "price": price, "balance": self.bot.account_balance})

            elif result["sell_signal"] and not self.bot.in_position:
                self.bot.execute_trade(
                    "SELL", price, result["position_size"],
                    result["stop_loss"], result["take_profit"]
                )
                trades.append({"type": "SELL", "price": price, "balance": self.bot.account_balance})

            # exit trade if SL/TP hit
            exit_msg = self.bot.check_exit_conditions(price)
            if exit_msg:
                trades.append({"type": "EXIT", "price": price, "balance": self.bot.account_balance})

            equity_curve.append(self.bot.account_balance)

        results_df = pd.DataFrame(trades)
        equity_df = pd.DataFrame({"Equity": equity_curve})

        # Save results
        results_df.to_csv("backtest_trades.csv", index=False)
        equity_df.to_csv("equity_curve.csv", index=False)

        # Show summary
        self._print_summary(results_df, equity_curve)

        return results_df, equity_df

    def _print_summary(self, trades: pd.DataFrame, equity_curve: list):
        if trades.empty:
            print("No trades executed.")
            return

        total_trades = len(trades[trades["type"].isin(["BUY", "SELL"])])
        wins = trades[trades["type"] == "EXIT"]["balance"].diff().fillna(0)
        win_trades = (wins > 0).sum()
        loss_trades = (wins < 0).sum()
        win_rate = (win_trades / (win_trades + loss_trades) * 100) if (win_trades + loss_trades) > 0 else 0

        final_balance = equity_curve[-1]
        profit = final_balance - self.initial_balance
        max_drawdown = (max(equity_curve) - min(equity_curve)) / max(equity_curve) * 100 if max(equity_curve) > 0 else 0

        print("\n=== Backtest Summary ===")
        print(f"Initial Balance: {self.initial_balance:.2f}")
        print(f"Final Balance:   {final_balance:.2f}")
        print(f"Total Trades:    {total_trades}")
        print(f"Win Rate:        {win_rate:.2f}%")
        print(f"Net Profit:      {profit:.2f}")
        print(f"Max Drawdown:    {max_drawdown:.2f}%")
        print("========================\n")


if __name__ == "__main__":
    backtester = Backtester(initial_balance=10000)
    trades, equity = backtester.run_backtest("your_data.csv")  # <-- replace with your CSV
    print(trades.head())
