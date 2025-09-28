import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

class MomentumBot:

    def calculate_stop_loss_take_profit(self, entry_price, trend, atr, risk_reward_ratio=2):
        """Calculate stop-loss and take-profit levels based on ATR and trend direction."""
        if atr is None or atr == 0:
            return 0, 0
        if trend == "UPTREND":
            stop_loss = entry_price - atr
            take_profit = entry_price + atr * risk_reward_ratio
        elif trend == "DOWNTREND":
            stop_loss = entry_price + atr
            take_profit = entry_price - atr * risk_reward_ratio
        else:
            stop_loss = entry_price - atr
            take_profit = entry_price + atr * risk_reward_ratio
        return stop_loss, take_profit

    def calculate_position_size(self, price, atr, risk_per_trade=0.02, risk_multiplier=2):
        """Calculate position size based on volatility and account balance"""
        if atr is None or atr == 0:
            return 0
        risk_amount = self.account_balance * risk_per_trade
        stop_distance = atr * risk_multiplier
        position_size = risk_amount / stop_distance
        return position_size

    def calculate_atr(self, high_prices, low_prices, close_prices, window=14):
        """Calculate Average True Range (ATR)"""
        import pandas as pd
        if len(high_prices) < window + 1:
            return None
        high = pd.Series(high_prices)
        low = pd.Series(low_prices)
        close = pd.Series(close_prices)
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=window).mean()
        return atr.iloc[-1] if not atr.empty else None
    # Example method: Use API key for a broker request
    def get_account_info(self):
        """Example: Use the API key to make a broker API request (pseudo-code)."""
        import requests
        if not self.api_key:
            raise ValueError("API key is not set. Please set BROKER_API_KEY env variable or pass api_key to the bot.")
        # Example endpoint (replace with your broker's real endpoint)
        url = "https://api.broker.com/v1/account"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        # This is a placeholder request. Replace with your broker's actual API usage.
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Broker API error: {response.status_code} {response.text}")
    # --- Additional Technical Indicators ---
    def calculate_rsi(self, prices, window=14):
        """Calculate Relative Strength Index (RSI)"""
        if len(prices) < window + 1:
            return None
        series = pd.Series(prices)
        delta = series.diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        avg_gain = gain.rolling(window=window, min_periods=window).mean()
        avg_loss = loss.rolling(window=window, min_periods=window).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if not rsi.empty else None

    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculate MACD and Signal Line"""
        if len(prices) < slow + signal:
            return None, None
        series = pd.Series(prices)
        ema_fast = series.ewm(span=fast, adjust=False).mean()
        ema_slow = series.ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        return macd.iloc[-1], signal_line.iloc[-1]

    def calculate_bollinger_bands(self, prices, window=20, num_std=2):
        """Calculate Bollinger Bands"""
        if len(prices) < window:
            return None, None, None
        series = pd.Series(prices)
        sma = series.rolling(window=window).mean()
        std = series.rolling(window=window).std()
        upper_band = sma + (num_std * std)
        lower_band = sma - (num_std * std)
        return upper_band.iloc[-1], sma.iloc[-1], lower_band.iloc[-1]
    def __init__(self, initial_balance=10000, api_key=None):
        import os
        self.account_balance = initial_balance
        self.position_size = 0
        self.stop_loss = 0
        self.take_profit = 0
        self.in_position = False
        self.entry_price = 0
        # API key management
        self.api_key = api_key or os.environ.get('BROKER_API_KEY')

    def set_api_key(self, api_key):
        """Set or update the broker API key."""
        self.api_key = api_key

    # Basic price movement methods
    def moving_up(self, prev_price, price):
        return price > prev_price

    def moving_down(self, prev_price, price):
        return price < prev_price

    # EMA Calculation
    def calculate_ema(self, prices, window):
        """Calculate Exponential Moving Average"""
        if len(prices) < window:
            return None
        return pd.Series(prices).ewm(span=window, adjust=False).mean().iloc[-1]

    # Stochastic Oscillator with EMA smoothing
    def calculate_stochastic(self, high_prices, low_prices, close_prices, k_period=14, d_period=3):
        """Calculate Stochastic Oscillator with EMA smoothing"""
        if len(close_prices) < k_period + d_period:
            return None, None
        
        highs = pd.Series(high_prices)
        lows = pd.Series(low_prices)
        closes = pd.Series(close_prices)
        
        # Calculate %K
        lowest_low = lows.rolling(window=k_period).min()
        highest_high = highs.rolling(window=k_period).max()
        
        raw_k = ((closes - lowest_low) / (highest_high - lowest_low)) * 100
        
        # Apply EMA smoothing to %K and %D
        k_percent = raw_k.ewm(span=d_period, adjust=False).mean()
        d_percent = k_percent.ewm(span=d_period, adjust=False).mean()
        
        return k_percent.iloc[-1] if not k_percent.empty else None, d_percent.iloc[-1] if not d_percent.empty else None

    def get_stochastic_signal(self, k, d, overbought=80, oversold=20):
        """Generate signals from Stochastic Oscillator"""
        if k is None or d is None:
            return None, "NO_DATA"
        
        if k < oversold and d < oversold:
            return "BUY", "Stochastic oversold"
        elif k > overbought and d > overbought:
            return "SELL", "Stochastic overbought"
        elif k > d:
            return "BUY", "Stochastic bullish"
        elif k < d:
            return "SELL", "Stochastic bearish"
        
        return None, "NO_SIGNAL"

    # Awesome Oscillator with periods 1 and 34
    def calculate_awesome_oscillator(self, high_prices, low_prices, fast_period=1, slow_period=34):
        """Calculate Awesome Oscillator (AO)"""
        if len(high_prices) < slow_period:
            return None, None
        
        # Calculate median price (High + Low) / 2
        median_prices = [(high + low) / 2 for high, low in zip(high_prices, low_prices)]
        
        # Calculate SMAs
        sma_fast = pd.Series(median_prices).rolling(window=fast_period).mean()
        sma_slow = pd.Series(median_prices).rolling(window=slow_period).mean()
        
        # Calculate AO
        ao = sma_fast - sma_slow
        
        current_ao = ao.iloc[-1] if not ao.empty else None
        prev_ao = ao.iloc[-2] if len(ao) > 1 else None
        
        return current_ao, prev_ao

    def get_ao_signal(self, current_ao, prev_ao):
        """Generate signals based on Awesome Oscillator"""
        if current_ao is None or prev_ao is None:
            return None, "NO_DATA"
        
        if prev_ao <= 0 and current_ao > 0:
            return "BUY", "AO crossed above zero"
        elif prev_ao >= 0 and current_ao < 0:
            return "SELL", "AO crossed below zero"
        
        return None, "NO_SIGNAL"

    # EMA-based trend detection
    def detect_trend_ema(self, ema_13, ema_20, ema_50, current_price):
        """Determine trend strength based on EMA alignment"""
        if any(ema is None for ema in [ema_13, ema_20, ema_50]):
            return "NEUTRAL", 0
        
        # EMA alignment conditions
        bullish_alignment = ema_13 > ema_20 > ema_50 and current_price > ema_13
        bearish_alignment = ema_13 < ema_20 < ema_50 and current_price < ema_13
        
        if bullish_alignment:
            return "UPTREND", 0.5
        elif bearish_alignment:
            return "DOWNTREND", 0.5
        else:
            return "NEUTRAL", 0

    # Momentum strategy
    def momentum_strategy(self, price_history, high_prices, low_prices, close_prices, volume_data=None):
        """Momentum strategy using EMA, Stochastic, and Awesome Oscillator"""
        
        if len(price_history) < 50:
            return {
                'buy_signal': False,
                'sell_signal': False,
                'stoch_k': None,
                'stoch_d': None,
                'trend': "NEUTRAL",
                'position_size': 0,
                'stop_loss': 0,
                'take_profit': 0,
                'ao_current': None,
                'ao_signal': None,
                'signals': ["No consensus"],
                'ema_13': None,
                'ema_20': None,
                'ema_50': None
            }

        # --- 2 out of 3 consensus logic ---
        ema_13 = self.calculate_ema(price_history, 13)
        ema_20 = self.calculate_ema(price_history, 20)
        ema_50 = self.calculate_ema(price_history, 50)
        stoch_k, stoch_d = self.calculate_stochastic(high_prices, low_prices, close_prices)
        stoch_signal, stoch_reason = self.get_stochastic_signal(stoch_k, stoch_d)
        ao_current, ao_prev = self.calculate_awesome_oscillator(high_prices, low_prices, 1, 34)
        ao_signal, ao_reason = self.get_ao_signal(ao_current, ao_prev)
        current_price = price_history[-1]
        trend, strength = self.detect_trend_ema(ema_13, ema_20, ema_50, current_price)

        ema_buy = ema_13 is not None and ema_20 is not None and ema_50 is not None and (ema_13 > ema_20 > ema_50 and current_price > ema_13)
        ema_sell = ema_13 is not None and ema_20 is not None and ema_50 is not None and (ema_13 < ema_20 < ema_50 and current_price < ema_13)
        stoch_buy = stoch_signal == "BUY"
        stoch_sell = stoch_signal == "SELL"
        ao_buy = ao_signal == "BUY"
        ao_sell = ao_signal == "SELL"

        buy_votes = sum([ema_buy, stoch_buy, ao_buy])
        sell_votes = sum([ema_sell, stoch_sell, ao_sell])

        final_buy_signal = buy_votes >= 2
        final_sell_signal = sell_votes >= 2

        if final_buy_signal:
            agreed = []
            if ema_buy: agreed.append("EMA bullish alignment")
            if stoch_buy: agreed.append("Stochastic BUY")
            if ao_buy: agreed.append("AO BUY")
            signals = ["BUY: " + ", ".join(agreed)]
        elif final_sell_signal:
            agreed = []
            if ema_sell: agreed.append("EMA bearish alignment")
            if stoch_sell: agreed.append("Stochastic SELL")
            if ao_sell: agreed.append("AO SELL")
            signals = ["SELL: " + ", ".join(agreed)]
        else:
            signals = ["No consensus"]

        # Calculate position size and risk levels
        position_size = 0
        stop_loss = 0
        take_profit = 0
        atr = self.calculate_atr(high_prices, low_prices, close_prices)
        if final_buy_signal or final_sell_signal:
            position_size = self.calculate_position_size(current_price, atr)
            stop_loss, take_profit = self.calculate_stop_loss_take_profit(current_price, trend, atr)

        return {
            'buy_signal': final_buy_signal,
            'sell_signal': final_sell_signal,
            'stoch_k': stoch_k,
            'stoch_d': stoch_d,
            'trend': trend,
            'position_size': position_size,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'ao_current': ao_current,
            'ao_signal': ao_signal,
            'signals': signals,
            'ema_13': ema_13,
            'ema_20': ema_20,
            'ema_50': ema_50
        }

    def check_exit_conditions(self, current_price):
        """Check if we need to exit position due to stop-loss or take-profit"""
        if not self.in_position:
            return None
            
        pnl = (current_price - self.entry_price) * self.position_size
        
        if (self.entry_price > self.stop_loss and current_price <= self.stop_loss) or \
           (self.entry_price < self.stop_loss and current_price >= self.stop_loss):
            self.account_balance += self.position_size * current_price
            self.in_position = False
            result = f"🛑 STOP-LOSS | P&L: ${pnl:.2f}"
            self._reset_position()
            return result
            
        elif (self.entry_price < self.take_profit and current_price >= self.take_profit) or \
             (self.entry_price > self.take_profit and current_price <= self.take_profit):
            self.account_balance += self.position_size * current_price
            self.in_position = False
            result = f"🎯 TAKE-PROFIT | P&L: ${pnl:.2f}"
            self._reset_position()
            return result
            
        return None

    def _reset_position(self):
        """Reset position parameters after exit"""
        self.position_size = 0
        self.stop_loss = 0
        self.take_profit = 0
        self.entry_price = 0