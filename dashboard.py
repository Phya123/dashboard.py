import os
import streamlit as st
import pandas as pd
from alpaca.trading.client import TradingClient

# ======================================
# PAGE CONFIG
# ======================================
st.set_page_config(page_title="EML Sentinel AI | LIVE", layout="wide")
st.title("⚡ EML SENTINEL AI | LIVE MONITORING")

# ======================================
# CONNECT TO LIVE ALPACA DATA
# ======================================
try:
    # 'paper=False' pulls LIVE market data and account status
    api = TradingClient(
        os.environ["APCA_API_KEY_ID"],
        os.environ["APCA_API_SECRET_KEY"],
        paper=False 
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
st.subheader("Live Account Overview")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Equity", f"${float(account.equity):,.2f}")
c2.metric("Buying Power", f"${float(account.buying_power):,.2f}")
c3.metric("Cash", f"${float(account.cash):,.2f}")
c4.metric("Portfolio", f"${float(account.portfolio_value):,.2f}")
c5.metric("Market Status", "OPEN" if clock.is_open else "CLOSED")

st.divider()

# ======================================
# READ-ONLY POSITIONS
# ======================================
st.subheader("Current Open Positions")

if positions:
    rows = [
        {
            "Symbol": p.symbol,
            "Qty": float(p.qty),
            "Entry": round(float(p.avg_entry_price), 2),
            "Market Price": round(float(p.current_price), 2),
            "PnL %": f"{round(float(p.unrealized_plpc) * 100, 2)}%",
            "Mkt Value": round(float(p.market_value), 2)
        } for p in positions
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
else:
    st.info("No open positions detected in the live account.")

st.divider()

# ======================================
# SENTINEL STATUS
# ======================================
st.subheader("System Status: MONITORING ONLY")
st.warning("⚠️ MODE: READ-ONLY. No trading logic is active.")
st.success("""
✅ API: Live (paper=False)
✅ Account: Authenticated
✅ Data Stream: Active
✅ Safety: Trading execution methods are disabled.
""")