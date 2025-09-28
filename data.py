import yfinance as yf
import time
import pandas as pd

def get_latest_data(symbol="EURUSD=X"):
    """Fetch the latest OHLCV data of a symbol from Yahoo Finance."""
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="1d", interval="1m")
        if not df.empty:
            return {
                'price': df["Close"].iloc[-1],
                'high': df["High"].iloc[-1],
                'low': df["Low"].iloc[-1],
                'open': df["Open"].iloc[-1],
                'volume': df["Volume"].iloc[-1]
            }
    except:
        pass
    return None

def get_historical_data(symbol="EURUSD=X", period="1d", interval="1m"):
    """Fetch historical OHLCV data for indicator calculations."""
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        if not df.empty:
            return {
                'prices': df["Close"].tolist(),
                'highs': df["High"].tolist(),
                'lows': df["Low"].tolist(),
                'opens': df["Open"].tolist(),
                'volumes': df["Volume"].tolist()
            }
    except:
        pass
    return {'prices': [], 'highs': [], 'lows': [], 'opens': [], 'volumes': []}

def stream_prices(symbol="EURUSD=X", interval=5):
    """Stream live prices with full OHLCV data every `interval` seconds (generator)."""
    prev_price = None
    historical_data = get_historical_data(symbol, period="1d", interval="1m")
    
    price_history = historical_data['prices']
    high_history = historical_data['highs']
    low_history = historical_data['lows']
    volume_history = historical_data['volumes']
    
    while True:
        latest_data = get_latest_data(symbol)
        if latest_data and latest_data['price']:
            current_price = latest_data['price']
            
            # Update history arrays
            price_history.append(current_price)
            high_history.append(latest_data['high'])
            low_history.append(latest_data['low'])
            volume_history.append(latest_data['volume'])
            
            # Keep last 200 data points
            if len(price_history) > 200:
                price_history = price_history[-200:]
                high_history = high_history[-200:]
                low_history = low_history[-200:]
                volume_history = volume_history[-200:]
            
            yield prev_price, current_price, price_history, high_history, low_history, volume_history
            prev_price = current_price
        time.sleep(interval)