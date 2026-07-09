import pandas as pd
import pandas_ta as ta

def run_scanner(data):
    """Expects dataframe with ['close', 'high', 'low']"""
    if len(data) < 200: return None
    
    df = data.copy()
    df['ema20'] = ta.ema(df['close'], length=20)
    df['ema50'] = ta.ema(df['close'], length=50)
    df['sma200'] = ta.sma(df['close'], length=200)
    df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    
    latest = df.iloc[-1]
    
    status = "HOLD"
    if latest['close'] > latest['ema20'] > latest['ema50']: status = "BUY WATCH"
    elif latest['close'] < latest['ema20'] < latest['ema50']: status = "SELL WATCH"
    
    return {
        "price": latest['close'],
        "ema20": latest['ema20'],
        "ema50": latest['ema50'],
        "sma200": latest['sma200'],
        "atr": latest['atr'],
        "status": status
    }