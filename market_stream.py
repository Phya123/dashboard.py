import pandas as pd
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame


WATCHLIST = [
    "SPY",
    "QQQ",
    "NVDA",
    "AAPL",
    "MSFT",
    "AMD",
    "META",
    "AMZN",
    "GOOGL",
    "TSLA",
    "LMT",
    "XLE",
    "ASML",
    "TSM",
    "NVS"
]


def get_live_market_stream(data_client):

    results = []

    for symbol in WATCHLIST:

        try:

            request = StockBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=TimeFrame.Minute,
                limit=2
            )


            bars = data_client.get_stock_bars(
                request
            )


            df = bars.df


            if df.empty:
                continue


            if isinstance(df.index, pd.MultiIndex):

                df = df.xs(symbol)


            latest = df.iloc[-1]


            results.append(
                {
                    "Symbol": symbol,
                    "Price": round(float(latest["close"]), 2),
                    "Open": round(float(latest["open"]), 2),
                    "High": round(float(latest["high"]), 2),
                    "Low": round(float(latest["low"]), 2),
                    "Volume": int(latest["volume"]),
                    "Change": round(
                        float(latest["close"]) - float(latest["open"]),
                        2
                    )
                }
            )


        except Exception as e:

            results.append(
                {
                    "Symbol": symbol,
                    "Price": "ERROR",
                    "Open": "-",
                    "High": "-",
                    "Low": "-",
                    "Volume": "-",
                    "Change": str(e)
                }
            )


    return pd.DataFrame(results)
