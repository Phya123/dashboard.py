import os
from datetime import datetime

import pandas as pd
import streamlit as st

from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from performance import (
    get_account_performance,
    get_symbol_statistics,
    get_equity_curve,
    get_open_positions,
    get_closed_trades
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
# SYMBOLS
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

    st.error(
        "Missing Alpaca API credentials."
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
# HELPERS
# ==========================

def money(value):

    try:
        return f"${float(value):,.2f}"

    except:
        return "$0.00"



def safe_float(value):

    try:
        return float(value)

    except:
        return 0.0



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

st.subheader(
    "💰 Account"
)


try:

    account = trading_client.get_account()

    clock = trading_client.get_clock()


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Equity",
        money(account.equity)
    )


    col2.metric(
        "Cash",
        money(account.cash)
    )


    col3.metric(
        "Buying Power",
        money(account.buying_power)
    )


    col4.metric(
        "Market",
        "OPEN" if clock.is_open else "CLOSED"
    )


except Exception as e:

    st.error(
        f"Account Error: {e}"
    )



# ==========================
# POSITIONS
# ==========================

st.divider()

st.subheader("📈 Performance")

try:

    stats = load_performance()

    a, b, c, d, e = st.columns(5)

    a.metric("Trades", stats.get("trades", 0))
    b.metric("Wins", stats.get("wins", 0))
    c.metric("Losses", stats.get("losses", 0))
    d.metric("Win Rate", f'{stats.get("win_rate", 0)}%')
    e.metric("Total P/L", money(stats.get("total_pnl", 0)))

except Exception as e:
    st.error(f"Performance Error: {e}")



# ==========================
# SCANNER
# ==========================

st.divider()

st.subheader(
    "🔍 Live Scanner"
)


try:

    scan = run_scanner(
        SYMBOLS,
        data_client
    )


    scan_df = pd.DataFrame(scan)


    st.dataframe(
        scan_df,
        use_container_width=True
    )


except Exception as e:

    st.error(
        f"Scanner Error: {e}"
    )



# ==========================
# PERFORMANCE
# ==========================

from performance import (
    get_account_performance,
    get_symbol_statistics,
    get_equity_curve,
    get_open_positions,
    get_closed_trades
)



# ==========================
# CHARTS
# ==========================

st.divider()

st.subheader(
    "📊 Market Charts"
)


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


        if isinstance(
            bars.index,
            pd.MultiIndex
        ):

            bars = bars.xs(selected)


        fig = create_price_chart(
            bars,
            selected
        )


        if fig:

            st.plotly_chart(
                fig,
                use_container_width=True
            )


except Exception as e:

    st.error(
        f"Chart Error: {e}"
    )



# ==========================
# TRADE JOURNAL
# ==========================

st.divider()

st.subheader(
    "📖 Trade Journal"
)


try:

    journal = load_trade_journal()


    if not journal.empty:

        st.dataframe(
            journal,
            use_container_width=True
        )

    else:

        st.info(
            "No trades logged yet"
        )


except Exception as e:

    st.error(e)



# ==========================
# SYMBOL STATS
# ==========================

st.divider()

st.subheader(
    "📊 Symbol Statistics"
)


try:

    symbol_stats = load_symbol_stats()


    if not symbol_stats.empty:

        st.dataframe(
            symbol_stats,
            use_container_width=True
        )


except Exception as e:

    st.error(e)



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
    "EML SENTINEL Dashboard is read-only. No orders can be placed here."
)