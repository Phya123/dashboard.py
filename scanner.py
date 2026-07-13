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

def get_symbol_data(symbol, data_client):

    try:

        request = StockBarsRequest(
            symbol_or_symbols=[symbol],
            timeframe=TimeFrame.Minute,
            limit=250
        )

        bars = data_client.get_stock_bars(
            request
        )

        df = bars.df

        if df is None or df.empty:
            print(f"{symbol} NO DATA")
            return None


        if isinstance(df.index, pd.MultiIndex):

            df = df.xs(symbol)


        df = df.dropna()

        return df


    except Exception as e:

        print(f"{symbol} DATA ERROR: {e}")

        return None



# ==========================
# ATR CALCULATION
# ==========================

def calculate_atr(df):

    high = df["high"]
    low = df["low"]
    close = df["close"]


    true_range = pd.concat(
        [
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs()
        ],
        axis=1
    ).max(axis=1)


    return (
        true_range
        .rolling(ATR_PERIOD)
        .mean()
        .iloc[-1]
    )



# ==========================
# ANALYZE SYMBOL
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

# Calculate moving averages only if enough data exists
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


    volatility = (
        atr / price
    ) * 100



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

        "Price": round(
            price,
            2
        ),

        "Trend": trend,

        "Fast MA": round(
            float(fast),
            2
        ),

        "Slow MA": round(
            float(slow),
            2
        ),

        "MA200": round(
            float(ma200),
            2
        ),

        "ATR": round(
            float(atr),
            4
        ),

        "Volatility %": round(
            float(volatility),
            3
        ),

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
                       
