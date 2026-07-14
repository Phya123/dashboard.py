import os
from datetime import datetime

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from scanner import (
    run_scanner,
    get_symbol_data
)

from charts import create_candlestick_chart

from performance import (
    load_performance,
    load_trade_journal,
    load_symbol_stats
)

    
# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="EML SENTINEL AI COMMAND CENTER",
    page_icon="🤖",
    layout="wide"
)


# ==========================
# HEDGE FUND WATCHLIST
# ==========================

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


# ==========================
# SENTINEL SYMBOLS
# ==========================

SYMBOLS = [
    "LMT",
    "SPCX",
    "DEO",
    "NVS",
    "TSM",
    "ASML",
    "QQQ",
    "SPY",
    "AAPL",
    "XLE",
    "NVDA"
]


# ==========================
# ALPACA CONNECTION
# ==========================

API_KEY = (
    os.getenv("APCA_API_KEY_ID")
    or os.getenv("ALPACA_API_KEY")
)

SECRET_KEY = (
    os.getenv("APCA_API_SECRET_KEY")
    or os.getenv("ALPACA_SECRET_KEY")
)


if not API_KEY or not SECRET_KEY:
    st.error("Missing Alpaca API credentials")
    st.stop()


@st.cache_resource
def get_clients():

    trading = TradingClient(
        API_KEY,
        SECRET_KEY,
        paper=False
    )

    data = StockHistoricalDataClient(
        API_KEY,
        SECRET_KEY
    )

    return trading, data


trading_client, data_client = get_clients()



# ==========================
# HELPERS
# ==========================

def money(value):

    try:
        return f"${float(value):,.2f}"

    except:
        return "$0.00"



# ==========================
# HEADER
# ==========================

st.title(
    "🤖 EML SENTINEL AI COMMAND CENTER"
)

st.caption(
    "LIVE Alpaca Monitor | Dashboard Trading Disabled"
)



# ==========================
# ACCOUNT
# ==========================

st.subheader("💰 Account")


try:

    account = trading_client.get_account()
    clock = trading_client.get_clock()


    c1,c2,c3,c4 = st.columns(4)


    c1.metric(
        "Equity",
        money(account.equity)
    )

    c2.metric(
        "Cash",
        money(account.cash)
    )

    c3.metric(
        "Buying Power",
        money(account.buying_power)
    )

    c4.metric(
        "Market",
        "OPEN" if clock.is_open else "CLOSED"
    )


except Exception as e:

    st.error(e)



# ============================================================
# LIVE MARKET DATA LOADER
# ============================================================

def get_live_chart_data(symbol):

    try:

        request = StockBarsRequest(
            symbol_or_symbols=[symbol],
            timeframe=TimeFrame.Minute,
            limit=100
        )

        bars = data_client.get_stock_bars(request)

        df = bars.df


        if df.empty:
            return None


        # Alpaca returns multi-index
        if "symbol" in df.index.names:

            df = df.xs(
                symbol,
                level="symbol"
            )


        # Make sure columns are lowercase

        df.columns = [
            c.lower()
            for c in df.columns
        ]


        return df


    except Exception as e:

        st.error(
            f"Market data error {symbol}: {e}"
        )

        return None

        else:
            st.warning("Price data unavailable")

except Exception as e:
    st.error("Live Market Terminal temporarily unavailable")
    st.caption(str(e))


# ==========================
# POSITIONS
# ==========================

st.divider()

st.subheader(
    "📊 Open Positions"
)


try:

    positions = trading_client.get_all_positions()


    if positions:

        rows=[]

        for p in positions:

            rows.append({

                "Symbol":p.symbol,
                "Qty":p.qty,
                "Entry":p.avg_entry_price,
                "Current":p.current_price,
                "P/L":p.unrealized_pl

            })


        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True
        )

    else:

        st.info(
            "No open positions"
        )


except Exception as e:

    st.error(e)



# ==========================
# SCANNER
# ==========================

st.divider()

st.subheader(
    "🔍 SENTINEL SCANNER"
)


try:

    scan = run_scanner(
        SYMBOLS,
        data_client
    )


    st.dataframe(
        pd.DataFrame(scan),
        use_container_width=True
    )


except Exception as e:

    st.error(
        f"Scanner Error {e}"
    )



# ==========================
# HEDGE FUND WATCHLIST
# ==========================

st.divider()

st.subheader(
    "🏦 Institutional Watchlist"
)


try:

    watch = run_scanner(
        WATCHLIST,
        data_client
    )


    st.dataframe(
        pd.DataFrame(watch),
        use_container_width=True
    )


except Exception as e:

    st.error(e)



# ==========================
# TRADE JOURNAL
# ==========================

st.divider()

st.subheader(
    "📖 Trade Journal"
)


try:

    journal = load_trade_journal()

    st.dataframe(
        journal,
        use_container_width=True
    )


except Exception as e:

    st.warning(e)



# ==========================
# SYMBOL STATS
# ==========================

st.divider()

st.subheader(
    "📊 Symbol Performance"
)


try:

    stats = load_symbol_stats()

    st.dataframe(
        stats,
        use_container_width=True
    )


except Exception as e:

    st.warning(e)



# ==========================
# FOOTER
# ==========================

st.divider()

st.write(
    "Last Update:",
    datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
)


st.caption(
    "EML SENTINEL is READ ONLY. No trading functions exist in this dashboard."
)
