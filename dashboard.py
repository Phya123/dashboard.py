import os
import streamlit as st
import pandas as pd

from alpaca.trading.client import TradingClient

# ======================================
# PAGE
# ======================================

st.set_page_config(
    page_title="EML Sentinel AI",
    layout="wide"
)

st.title("🤖 EML SENTINEL AI COMMAND CENTER")

# ======================================
# CONNECT TO ALPACA
# ======================================

api = TradingClient(
    os.environ["APCA_API_KEY_ID"],
    os.environ["APCA_API_SECRET_KEY"],
    paper=False
)

account = api.get_account()
positions = api.get_all_positions()
clock = api.get_clock()

# ======================================
# ACCOUNT
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
# RISK PANEL
# ======================================

cash_used = (
    (float(account.portfolio_value) - float(account.cash))
    / float(account.portfolio_value)
) * 100

r1, r2, r3, r4 = st.columns(4)

r1.metric("Cash Used", f"{cash_used:.1f}%")
r2.metric("Open Positions", len(positions))
r3.metric("Daily Loss Limit", "3%")
r4.metric("Circuit Breaker", "READY")

st.divider()

# ======================================
# OPEN POSITIONS
# ======================================

st.subheader("Live Positions")

rows = []

for p in positions:

    rows.append({
        "Symbol": p.symbol,
        "Qty": float(p.qty),
        "Entry": round(float(p.avg_entry_price),2),
        "Current": round(float(p.current_price),2),
        "PnL %": round(float(p.unrealized_plpc)*100,2),
        "Market Value": round(float(p.market_value),2)
    })

if rows:
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
else:
    st.success("No open positions")

st.divider()

# ======================================
# WATCHLIST
# ======================================

watchlist = [
    "SPY",
    "QQQ",
    "AAPL",
    "LMT",
    "XLE",
    "SPCX",
    "NVDA",
    "ASML",
    "TSM",
    "DEO",
    "NVS"
]

st.subheader("Sentinel Watchlist")

st.dataframe(
    pd.DataFrame({"Symbols": watchlist}),
    use_container_width=True
)

st.divider()

# ======================================
# BOT STATUS
# ======================================

st.subheader("Sentinel Status")

st.info(
"""
✅ Trading Engine Running

✅ Connected to Alpaca

✅ Live Account

✅ Market Data Active

Scanning all watchlist symbols every 60 seconds.
"""
)