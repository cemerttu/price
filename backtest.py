import pandas as pd
from bot import MomentumBot

if __name__ == "__main__":
    # Path to your historical CSV file
    csv_path = "your_data.csv"  # Change this to your actual file

    # Initialize your bot
    bot = MomentumBot()

    # Run backtest
    results = bot.backtest_from_csv(csv_path)

    # Show results
    print(results)
    # Optionally, save to a new CSV
    results.to_csv("backtest_results.csv", index=False)
