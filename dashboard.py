import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
from alpaca.trading.client import TradingClient
from charts import create_price_chart
from performance import load_performance
from scanner import run_scanner

st.set_page_config(page_title="EML SENTINEL", layout="wide")

# Connection
@st.cache_resource
def get_client():
    return TradingClient(os.getenv("APCA_API_KEY_ID"), os.getenv("APCA_API_SECRET_KEY"), paper=False)

client = get_client()

st.title("🤖 EML SENTINEL | LIVE MONITOR")
st.caption(f"Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Metrics
try:
    acc = client.get_account()
    pos = client.get_all_positions()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Equity", f"${float(acc.equity):,.2f}")
    col2.metric("Cash", f"${float(acc.cash):,.2f}")
    col3.metric("Buying Power", f"${float(acc.buying_power):,.2f}")
    col4.metric("Market", "OPEN" if client.get_clock().is_open else "CLOSED")
except Exception as e:
    st.error(f"Connection Error: {e}")

# Positions
st.subheader("📊 Open Positions")
if pos:
    df_pos = pd.DataFrame([p.__dict__ for p in pos])
    st.dataframe(df_pos[['symbol', 'qty', 'avg_entry_price', 'unrealized_plpc']], use_container_width=True)
else:
    st.info("No active positions.")

# Journal & Performance
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("📜 Trade Journal")
    if os.path.exists("trade_journal.csv"):
        st.dataframe(pd.read_csv("trade_journal.csv"), use_container_width=True)
with col_b:
    st.subheader("📈 Performance")
    stats = load_performance()
    st.write(stats)

# Auto-refresh
st.empty()
if st.button("Refresh Data"):
    st.rerun()