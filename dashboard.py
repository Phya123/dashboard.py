import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from charts import create_price_chart
from performance import load_performance
from scanner import run_scanner


# ==========================
# CONFIG
# ==========================

st.set_page_config(
    page_title="EML SENTINEL AI COMMAND CENTER",
    page_icon="🤖",
    layout="wide"
)

SYMBOLS = [
    "SPY",
    "QQQ",
    "AAPL",
    "LMT",
    "DEO",
    "ASML",
    "NVD",
    "TSM",
    "XLE"
]


# ==========================
# ALPACA CONNECTION
# ==========================

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

if not API_KEY or not SECRET_KEY:
    st.error(
        "Missing Alpaca API credentials. Add ALPACA_API_KEY and ALPACA_SECRET_KEY to your environment variables."
    )
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
# HEADER
# ==========================

st.title("🤖 EML SENTINEL AI COMMAND CENTER")

st.caption(
    "LIVE Alpaca Monitor | Dashboard Trading Disabled"
)


# ==========================
# ACCOUNT PANEL
# ==========================

try:

    account = trading_client.get_account()

    equity = float(account.equity)
    cash = float(account.cash)
    buying_power = float(account.buying_power)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Equity",
        f"${equity:,.2f}"
    )

    col2.metric(
        "Cash",
        f"${cash:,.2f}"
    )

    col3.metric(
        "Buying Power",
        f"${buying_power:,.2f}"
    )

    col4.metric(
        "Status",
        "LIVE"
    )


except Exception as e:

    st.error(
        f"Alpaca connection error: {e}"
    )


# ==========================
# POSITIONS
# ==========================

st.subheader("📊 Open Positions")


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
                "Market Value":p.market_value,
                "P/L":p.unrealized_pl,
                "P/L %":p.unrealized_plpc

            })

        df=pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.info(
            "No open positions"
        )


except Exception as e:

    st.error(e)



# ==========================
# LIVE SCANNER
# ==========================

st.subheader("🔍 Live Scanner")


try:

    scan = run_scanner(
        SYMBOLS,
        data_client
    )


    scan_df=pd.DataFrame(scan)

    st.dataframe(
        scan_df,
        use_container_width=True
    )


except Exception as e:

    st.error(
        f"Scanner error: {e}"
    )



# ==========================
# PERFORMANCE
# ==========================

st.subheader("📈 Performance")


try:

    stats = load_performance()


    c1,c2,c3,c4 = st.columns(4)


    c1.metric(
        "Trades",
        stats["trades"]
    )


    c2.metric(
        "Wins",
        stats["wins"]
    )


    c3.metric(
        "Losses",
        stats["losses"]
    )


    c4.metric(
        "Win Rate",
        f'{stats["win_rate"]}%'
    )


except:

    st.info(
        "No performance data yet"
    )



# ==========================
# CHARTS
# ==========================

st.subheader("📊 Market Charts")


selected = st.selectbox(
    "Select Symbol",
    SYMBOLS
)


try:

    request = StockBarsRequest(
        symbol_or_symbols=selected,
        timeframe=TimeFrame.Minute,
        limit=100
    )


    bars = data_client.get_stock_bars(
        request
    ).df


    if not bars.empty:

        fig=create_price_chart(
            bars,
            selected
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


except Exception as e:

    st.error(e)



# ==========================
# LAST UPDATE
# ==========================

st.divider()

st.write(
    "Last Update:",
    datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
)