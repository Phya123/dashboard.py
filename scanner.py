import pandas as pd
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame


# ==========================
# SETTINGS
# ==========================

FAST_MA = 20
SLOW_MA = 50
MA200 = 200
ATR_PERIOD = 14


# ==========================
# GET DATA
# ==========================

def analyze_symbol(symbol, data_client):

    df = get_symbol_data(
        symbol,
        data_client
    )

    if df is None or df.empty:

        return {
            "Symbol": symbol,
            "Price": "N/A",
            "Trend": "NO DATA",
            "Fast MA": "-",
            "Slow MA": "-",
            "MA200": "-",
            "ATR": "-",
            "Volatility": "-",
            "Signal": "BAD DATA"
        }

    close = df["close"]

    price = float(close.iloc[-1])

    fast = (
        close.rolling(FAST_MA).mean().iloc[-1]
        if len(df) >= FAST_MA
        else price
    )

    slow = (
        close.rolling(SLOW_MA).mean().iloc[-1]
        if len(df) >= SLOW_MA
        else price
    )

    ma200 = (
        close.rolling(MA200).mean().iloc[-1]
        if len(df) >= MA200
        else price
    )

    atr = calculate_atr(df)

    volatility = (atr / price) * 100

    if fast > slow:
        trend = "BULLISH"
    else:
        trend = "BEARISH"

    if price < ma200:
        signal = "BELOW MA200"
    elif volatility < 0.05:
        signal = "LOW VOLATILITY"
    elif trend == "BULLISH":
        signal = "WATCH BUY"
    else:
        signal = "WATCH"

    return {
        "Symbol": symbol,
        "Price": round(price, 2),
        "Trend": trend,
        "Fast MA": round(float(fast), 2),
        "Slow MA": round(float(slow), 2),
        "MA200": round(float(ma200), 2),
        "ATR": round(float(atr), 4),
        "Volatility %": round(float(volatility), 3),
        "Signal": signal
    }



# ==========================
# RUN SCANNER
# ==========================

def run_scanner(symbols, data_client):

    results = []


    for symbol in symbols:

        results.append(
            analyze_symbol(
                symbol,
                data_client
            )
        )


    return results
                       
