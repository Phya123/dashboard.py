import pandas as pd
from alpaca.data.requests import StockLatestBarRequest


# ==========================
# HEDGE FUND WATCHLIST
# DASHBOARD ONLY
# ==========================

WATCHLIST = [
    # Index
    "SPY",
    "QQQ",
    "DIA",
    "IWM",
    "VTI",

    # Mega Cap Tech
    "AAPL",
    "MSFT",
    "NVDA",
    "GOOGL",
    "AMZN",
    "META",
    "TSLA",
    "AVGO",
    "AMD",
    "ORCL",

    # Semiconductor / AI
    "TSM",
    "ASML",
    "MU",
    "ARM",
    "SMCI",

    # Financial
    "JPM",
    "GS",
    "MS",
    "BAC",
    "V",
    "MA",

    # Energy
    "XOM",
    "CVX",
    "COP",
    "SLB",
    "XLE",

    # Healthcare
    "LLY",
    "JNJ",
    "UNH",
    "NVS",
    "MRK",

    # Defense
    "LMT",
    "RTX",
    "NOC",
    "GD",

    # Consumer
    "COST",
    "WMT",
    "HD",
    "MCD"
]


# ==========================
# LIVE MARKET DATA
# ==========================

def get_live_market_stream(data_client):

    results = []

    try:

        request = StockLatestBarRequest(
            symbol_or_symbols=WATCHLIST
        )

        bars = data_client.get_stock_latest_bar(
            request
        )


        for symbol, bar in bars.items():

            results.append(
                {
                    "Symbol": symbol,
                    "Price": round(
                        float(bar.close),
                        2
                    ),
                    "Volume": int(
                        bar.volume
                    ),
                    "Updated": bar.timestamp
                }
            )


        return pd.DataFrame(results)


    except Exception as e:

        return pd.DataFrame(
            {
                "Error": [
                    str(e)
                ]
            }
)
