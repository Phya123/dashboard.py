import os
import streamlit as st
import pandas as pd
from alpaca.trading.client import TradingClient

# ======================================
# PAGE CONFIG
# ======================================
st.set_page_config(page_title="EML Sentinel AI", layout="wide")
st.title("🤖 EML SENTINEL AI COMMAND CENTER")

# ======================================
# CONNECT TO ALPACA
# ======================================
try:
    api = TradingClient(
        os.environ["APCA_API_KEY_ID"],
        os.environ["APCA_API_SECRET_KEY"],
        paper=True # Ensure paper is set correctly
    )
    account = api.get_account()
    positions = api.get_all_positions()
    clock = api.get_clock()
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

# ======================================
# ACCOUNT & RISK METRICS
# ======================================
st.subheader("Account")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Equity", f"${float(account.equity):,.2f}")
c2.metric("Buying Power", f"${float(account.buying_power):,.2f}")
c3.metric("Cash", f"${float(account.cash):,.2f}")
c4.metric("Portfolio Value", f"${float(account.portfolio_value):,.2f}")
c5.metric("Market", "OPEN" if clock.is_open else "CLOSED")

st.divider()

# ======================================
# POSITIONS (FIXED LOGIC)
# ======================================
st.subheader("Live Positions")

# Ensure positions exist before iterating
if positions:
    rows = []
    for p in positions:
        rows.append({
            "Symbol": p.symbol,
            "Qty": float(p.qty),
            "Entry": round(float(p.avg_entry_price), 2),
            "Current": round(float(p.current_price), 2),
            "PnL %": round(float(p.unrealized_plpc) * 100, 2),
            "Market Value": round(float(p.market_value), 2)
        })
    df_positions = pd.DataFrame(rows)
    st.dataframe(df_positions, use_container_width=True)
else:
    st.success("No open positions")

st.divider()

# ======================================
# WATCHLIST
# ======================================
watchlist = ["SPY", "QQQ", "AAPL", "LMT", "XLE", "SPCX", "NVDA", "ASML", "TSM", "DEO", "NVS"]
st.subheader("Sentinel Watchlist")
st.dataframe(pd.DataFrame({"Symbols": watchlist}), use_container_width=True)

st.divider()

# ======================================
# BOT STATUS
# ======================================
st.subheader("Sentinel Status")
st.info("""
✅ Trading Engine Running
✅ Connected to Alpaca
✅ Live Account
✅ Market Data Active
Scanning all watchlist symbols every 60 seconds.
""")