import yfinance as yf
import pandas as pd
import numpy as np

def calculate_indicators(df):
    df['EMA_13'] = df['Close'].ewm(span=13, adjust=False).mean()
    df['EMA_23'] = df['Close'].ewm(span=23, adjust=False).mean()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['BB_MA'] = df['Close'].rolling(window=20).mean()
    df['BB_std'] = df['Close'].rolling(window=20).std()
    df['BB_upper'] = df['BB_MA'] + 2 * df['BB_std']
    df['BB_lower'] = df['BB_MA'] - 2 * df['BB_std']
    return df

def generate_signals(df):
    # Simple rule: Buy if Close > EMA_10 and RSI < 30, Sell if Close < EMA_10 and RSI > 70
    df['signal'] = 0
    df.loc[(df['Close'] > df['EMA_10']) & (df['RSI'] < 30), 'signal'] = 1  # Buy
    df.loc[(df['Close'] < df['EMA_10']) & (df['RSI'] > 70), 'signal'] = -1 # Sell
    return df

def main():
    ticker = 'AAPL'
    df = yf.download(ticker, period='1y', interval='1d')
    df = df.reset_index()
    # Flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join([str(i) for i in col if i]) for col in df.columns.values]
    print('Columns after flattening:', df.columns.tolist())
    # Try to use 'Close' or 'Close_AAPL' depending on column names
    close_col = 'Close' if 'Close' in df.columns else None
    for col in df.columns:
        if col.lower().startswith('close'):
            close_col = col
            break
    if not close_col:
        raise ValueError("No 'Close' column found. Columns: " + str(df.columns.tolist()))
    df = df.rename(columns={close_col: 'Close'})
    df = calculate_indicators(df)
    df = generate_signals(df)
    df = df.dropna()
    df.to_csv('your_data.csv', index=False)
    print('Sample data with indicators and signals saved to your_data.csv')

if __name__ == '__main__':
    main()
