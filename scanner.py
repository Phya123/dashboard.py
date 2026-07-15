# ============================================================
# EML SENTINEL
# INSTITUTIONAL MARKET SCANNER
# ============================================================

import pandas as pd

from alpaca.data.timeframe import TimeFrame


FAST_MA = 20
SLOW_MA = 50
MA200 = 200
ATR_PERIOD = 14


def calculate_atr(df):

    high = df["high"]
    low = df["low"]
    close = df["close"]

    tr = pd.concat(
        [
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)

    return tr.rolling(
        ATR_PERIOD
    ).mean().iloc[-1]



def analyze_symbol(symbol, market_data):

    try:

        df = market_data.get_bars(
            symbol,
            timeframe=TimeFrame.Minute,
            limit=200
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


        price = float(
            close.iloc[-1]
        )


        fast = (
            close.rolling(FAST_MA)
            .mean()
            .iloc[-1]
        )


        slow = (
            close.rolling(SLOW_MA)
            .mean()
            .iloc[-1]
        )


        ma200 = (
            close.rolling(MA200)
            .mean()
            .iloc[-1]
        )


        atr = calculate_atr(df)


        volatility = (
            atr / price * 100
            if price
            else 0
        )


        if fast > slow:

            trend = "BULLISH"

        else:

            trend = "BEARISH"


        if price < ma200:

            signal = "BELOW MA200"

        elif trend == "BULLISH":

            signal = "WATCH BUY"

        else:

            signal = "WATCH"



        return {

            "Symbol": symbol,
            "Price": round(price,2),
            "Trend": trend,
            "Fast MA": round(float(fast),2),
            "Slow MA": round(float(slow),2),
            "MA200": round(float(ma200),2),
            "ATR": round(float(atr),4),
            "Volatility": round(float(volatility),2),
            "Signal": signal

        }


    except Exception as e:

        print(
            f"Scanner error {symbol}: {e}"
        )

        return {

            "Symbol": symbol,
            "Price": "ERROR",
            "Trend": "-",
            "Signal": "ERROR"

        }



def run_scanner(symbols, data_client):

    from market_data import MarketDataEngine

    # Allow old dashboard calls to keep working
    if hasattr(data_client, "get_bars"):

        market_data = data_client

    else:

        market_data = MarketDataEngine(
            data_client
        )


    results = []


    for symbol in symbols:

        results.append(
            analyze_symbol(
                symbol,
                market_data
            )
        )


    return results
    
