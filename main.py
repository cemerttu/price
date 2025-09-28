from bot import MomentumBot
from data import stream_prices

# Initialize bot
bot = MomentumBot(initial_balance=10000)

print("🔄 Starting MOMENTUM STRATEGY Bot (EMA 13/20/50 + Stochastic + AO)...")
print(f"💰 Account Balance: ${bot.account_balance:,.2f}")
print("⏳ (Ctrl+C to stop)\n")

for (prev_price, price, price_history, 
     high_history, low_history, volume_history) in stream_prices("EURUSD=X", interval=10):
    
    if prev_price is None:
        continue

    # Check exit conditions
    exit_message = bot.check_exit_conditions(price)
    if exit_message:
        print(f"🔔 {exit_message} | Balance: ${bot.account_balance:,.2f}")

    # Run momentum strategy
    result = bot.momentum_strategy(
        price_history=price_history,
        high_prices=high_history,
        low_prices=low_history,
        close_prices=price_history,
        volume_data=volume_history
    )
    if not result or not isinstance(result, dict):
        continue

    if result['ema_13'] is not None and result['stoch_k'] is not None:
        # Debug: Print indicator values and consensus logic
        print(f"[DEBUG] EMA13: {result['ema_13']}, EMA20: {result['ema_20']}, EMA50: {result['ema_50']}")
        print(f"[DEBUG] Stoch K: {result['stoch_k']}, Stoch D: {result['stoch_d']}, AO: {result['ao_current']}, AO Signal: {result['ao_signal']}")
        print(f"[DEBUG] Buy consensus: {result['buy_signal']}, Sell consensus: {result['sell_signal']}")
        # Display indicators
        print(f"📊 EMA13: {result['ema_13']:.4f} | EMA20: {result['ema_20']:.4f} | EMA50: {result['ema_50']:.4f}")
        print(f"🎯 Stochastic: K={result['stoch_k']:.1f} | D={result['stoch_d']:.1f}")
        
        # Awesome Oscillator display
        ao_arrow = "🟢" if result['ao_current'] and result['ao_current'] > 0 else "🔴" if result['ao_current'] and result['ao_current'] < 0 else "⚪"
        ao_shape = "⬆️" if result['ao_signal'] == 'BUY' else "⬇️" if result['ao_signal'] == 'SELL' else "➡️"
        print(f"🚀 Awesome Oscillator: {ao_arrow}{ao_shape} {result['ao_current']:.4f}" if result['ao_current'] else f"🚀 Awesome Oscillator: {ao_arrow}{ao_shape} N/A")
        
        print(f"📈 Trend: {result['trend']}")
        
        # Show signals
        if result['signals']:
            print(f"📢 Signals: {', '.join(result['signals'])}")
        
        # Execute trades
        if result['buy_signal'] and not bot.in_position:
            trade_msg = bot.execute_trade("BUY", price, result['position_size'], result['stop_loss'], result['take_profit'])
            if trade_msg:
                print(f"🎯 {trade_msg}")
                print(f"💰 Remaining Balance: ${bot.account_balance:,.2f}")
            
        elif result['sell_signal'] and not bot.in_position:
            trade_msg = bot.execute_trade("SELL", price, result['position_size'], result['stop_loss'], result['take_profit'])
            if trade_msg:
                print(f"🎯 {trade_msg}")
                print(f"💰 Remaining Balance: ${bot.account_balance:,.2f}")

    print("-" * 80)