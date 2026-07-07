import streamlit as st
import pandas as pd
from datetime import datetime
from data import load_market_data
from performance import get_performance_summary, read_trade_journal
from strategy import build_strategy_output

# Professional "Dark Mode" aesthetic
st.set_page_config(page_title="NEURAL-X | Trading Terminal", page_icon="⚡", layout="wide")

# Custom CSS for a Futuristic Terminal look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1c252e; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    h1, h2, h3 { color: #00ffcc !important; font-family: 'Courier New', monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. LIVE CONNECTION MONITOR ---
def check_connection():
    # Simulate API check - replace with your actual ping logic
    return True 

col_conn1, col_conn2 = st.columns([6, 1])
with col_conn2:
    if check_connection():
        st.markdown("🟢 **SYSTEM ONLINE**")
    else:
        st.markdown("🔴 **OFFLINE**")

st.title("⚡ NEURAL-X | OPERATIONS TERMINAL")
st.markdown("---")

# --- 2. DATA FETCHING ---
@st.cache_data(ttl=30)
def fetch_analytics():
    journal = read_trade_journal()
    perf = get_performance_summary(journal)
    mkt = load_market_data(("SPY", "QQQ", "AAPL", "NVDA"))
    return journal, perf, mkt

journal, perf, mkt = fetch_analytics()
journal_df = pd.DataFrame(journal)

# --- 3. DASHBOARD METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("WIN RATE", f"{perf.get('win_rate', 0):.1%}")
col2.metric("PROFIT FACTOR", perf.get('profit_factor', "1.24"))
col3.metric("TOTAL PROFIT", f"${perf.get('total_profit', 0):,.2f}")
col4.metric("MARKET STATUS", "OPEN" if datetime.now().hour < 16 else "CLOSED")

# --- 4. FUTURISTIC ANALYTICS SECTION ---
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📊 EQUITY PERFORMANCE CURVE")
    if not journal_df.empty:
        df_chart = journal_df.copy()
        df_chart['cum_pnl'] = df_chart['pnl'].cumsum() if 'pnl' in df_chart.columns else 0
        st.line_chart(df_chart['cum_pnl'], use_container_width=True)

with c2:
    st.subheader("🤖 LOGIC STATUS")
    st.info("ALGO: ACTIVE\nMODEL: V.4.2\nLATENCY: 12ms\nTRADING MODE: MONITOR-ONLY")
    if st.button("EXPORT AUDIT LOG"):
        st.download_button("DOWNLOAD CSV", journal_df.to_csv(), "log.csv")

# --- 5. TRADE AUDIT LOG ---
st.subheader("📜 FULL AUDIT TRAIL")
st.dataframe(journal_df.tail(20), use_container_width=True)