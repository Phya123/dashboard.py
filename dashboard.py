import streamlit as st
import pandas as pd
from performance import get_performance_summary, read_trade_journal
from data import load_market_data

# Use this decorator to ensure data is only fetched when requested, 
# keeping the UI fast and efficient.
@st.cache_data(ttl=60)
def fetch_analytics():
    journal = read_trade_journal()
    perf = get_performance_summary(journal)
    return journal, perf

journal, perf = fetch_analytics()

st.title("Pro-Grade Trading Monitor")

# --- Institutional KPI Panel ---
# Buyers look for high-level metrics first.
col1, col2, col3, col4 = st.columns(4)
col1.metric("Win Rate", f"{perf.get('win_rate', 0):.1%}")
col2.metric("Profit Factor", perf.get('profit_factor', "N/A"))
col3.metric("Total Profit", f"${perf.get('total_profit', 0):,.2f}")
col4.metric("Max Drawdown", perf.get('max_drawdown', "0%"))

# --- Detailed Trade Journal ---
st.subheader("Trade Audit Log")
if not journal.empty:
    # Adding a search/filter feature increases value immediately
    search_term = st.text_input("Filter by Symbol:")
    display_df = journal[journal['symbol'].str.contains(search_term, case=False)] if search_term else journal
    st.dataframe(display_df, use_container_width=True)
else:
    st.info("Awaiting data...")