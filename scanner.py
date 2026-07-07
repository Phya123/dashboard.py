import pandas as pd
import numpy as np
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame


# ==========================
# SETTINGS
# ==========================

FAST_MA = 20
SLOW_MA = 50
ATR_PERIOD = 14


# ==========================
# GET MARKET DATA
# ==========================

def get_bars(symbol, data_client):

    try:

        request = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=TimeFrame.Minute,
            limit=100
        )

        bars = data_client.get_stock_bars(
            request
        ).df


        if bars.empty:
            return None


        if isinstance(
            bars.index,
            pd.MultiIndex
        ):

            bars = bars.xs(
                symbol
            )


        return bars


    except Exception:

        return None



# ==========================
# ANALYZE SYMBOL
# ==========================

def analyze_symbol(symbol, data_client):

    bars = get_bars(
        symbol,
        data_client
    )


    if bars is None or len(bars) < SLOW_MA:

        return {

            "Symbol":symbol,
            "Price":"N/A",
            "Trend":"NO DATA",
            "Fast MA":"-",
            "Slow MA":"-",
            "ATR":"-",
            "Volatility":"-",
            "Signal":"BAD DATA"

        }



    close = bars["close"]


    fast = close.rolling(
        FAST_MA
    ).mean().iloc[-1]


    slow = close.rolling(
        SLOW_MA
    ).mean().iloc[-1]


    price = close.iloc[-1]



    # ATR

    high = bars["high"]

    low = bars["low"]


    tr = pd.concat(
        [
            high-low,
            abs(high-close.shift()),
            abs(low-close.shift())
        ],
        axis=1
    ).max(axis=1)


    atr = tr.rolling(
        ATR_PERIOD
    ).mean().iloc[-1]



    volatility = (
        atr / price
    ) * 100



    if fast > slow:

        trend="BULLISH"

    else:

        trend="BEARISH"



    # signal logic

    if volatility < 0.05:

        signal="LOW VOLATILITY"


    elif trend=="BULLISH":

        signal="WATCH BUY"


    else:

        signal="WATCH"



    return {

        "Symbol":symbol,

        "Price":round(
            float(price),
            2
        ),

        "Trend":trend,

        "Fast MA":round(
            float(fast),
            2
        ),

        "Slow MA":round(
            float(slow),
            2
        ),

        "ATR":round(
            float(atr),
            4
        ),

        "Volatility %":round(
            float(volatility),
            3
        ),

        "Signal":signal

    }



# ==========================
# RUN SCANNER
# ==========================

def run_scanner(symbols, data_client):

    results=[]


    for symbol in symbols:

        result = analyze_symbol(
            symbol,
            data_client
        )

        results.append(
            result
        )


    return results