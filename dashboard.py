import streamlit as st
import pandas as pd
from data import load_market_data
from performance import get_performance_summary, read_trade_journal
from strategy import build_strategy_output

st.set_page_config(page_title="Professional Trading Monitor", page_icon="📈", layout="wide")

# --- DATA FETCHING WITH ERROR HANDLING ---
@st.cache_data(ttl=60)
def fetch_analytics():
    try:
        journal = read_trade_journal()
        perf = get_performance_summary(journal)
        market_data = load_market_data(("SPY", "QQQ", "AAPL", "NVDA", "TSM"))
        strategy = build_strategy_output(market_data)
        return journal, perf, strategy
    except Exception as e:
        return [], {}, []

journal, perf, strategy = fetch_analytics()

st.title("Trading Operations Monitor")
st.caption("Professional-grade monitoring environment.")

# --- 1. INSTITUTIONAL KPI PANEL ---
# These metrics define the 'worth' of the strategy to a potential buyer
col1, col2, col3, col4 = st.columns(4)
col1.metric("Win Rate", f"{perf.get('win_rate', 0):.1%}")
col2.metric("Profit Factor", perf.get('profit_factor', "N/A"))
col3.metric("Total Profit", f"${perf.get('total_profit', 0):,.2f}")
col4.metric("Strategy Efficiency", f"{perf.get('efficiency', 'N/A')}")

# --- 2. PERFORMANCE TREND CHART ---
st.subheader("Performance Equity Curve")
if journal:
    df_journal = pd.DataFrame(journal)
    # Convert 'timestamp' to datetime and sort for the chart
    if 'timestamp' in df_journal.columns:
        df_journal['timestamp'] = pd.to_datetime(df_journal['timestamp'])
        df_journal = df_journal.sort_values('timestamp')
        # Create a cumulative profit column for the chart
        df_journal['cumulative_profit'] = df_journal['pnl'].cumsum() if 'pnl' in df_journal.columns else 0
        st.line_chart(df_journal.set_index('timestamp')['cumulative_profit'])
    else:
        st.warning("Insufficient time-series data for chart.")
else:
    st.info("Performance data insufficient to plot trend.")

# --- 3. TRADE AUDIT LOG ---
st.subheader("Trade Audit Log")
journal_df = pd.DataFrame(journal)

if not journal_df.empty:
    search_term = st.text_input("🔍 Filter Audit Log by Symbol:")
    if search_term:
        display_df = journal_df[journal_df['symbol'].str.contains(search_term, case=False, na=False)]
    else:
        display_df = journal_df
    
    st.dataframe(display_df, use_container_width=True)
else:
    st.info("No trade activity recorded in the journal.")

# --- 4. STRATEGY WATCHLIST ---
st.subheader("Current Strategy Signals")
if strategy:
    watchlist = [{"Symbol": s.symbol, "Action": s.action, "Price": f"${s.price:,.2f}"} for s in strategy]
    st.table(pd.DataFrame(watchlist))