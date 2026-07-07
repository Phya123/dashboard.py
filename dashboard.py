import streamlit as st
import pandas as pd

# Set up the futuristic look
st.set_page_config(page_title="NEURAL-X TERMINAL", layout="wide")
st.markdown("""<style>.stMetric {background-color: #0e1117; border: 1px solid #00ffcc; border-radius: 5px;}</style>""", unsafe_allow_html=True)

# --- 1. HEADER & SYSTEM STATUS ---
col_head1, col_head2 = st.columns([4, 1])
col_head1.title("⚡ NEURAL-X | LIVE MONITOR")
col_head2.markdown("### 🟢 ONLINE")
st.markdown("---")

# --- 2. PERFORMANCE KPIs (The "Worth" Metrics) ---
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Win Rate", "73.8%")
c2.metric("Profit Factor", "2.41")
c3.metric("Total Profit", "$148.63")
c4.metric("Avg Winner", "+3.1%")
c5.metric("Avg Loser", "-1.2%")

# --- 3. MARKET SENTIMENT & EML SENTINEL ---
col_a, col_b = st.columns([2, 1])
with col_a:
    st.subheader("📊 MARKET TRENDS")
    # Data from your provided stats
    trend_data = {"Symbol": ["QQQ", "SPCX", "SPY", "NVDA", "XLE"], "Perf": [8.2, 6.9, 5.8, 3.4, -0.8]}
    st.bar_chart(pd.DataFrame(trend_data).set_index("Symbol"))

with col_b:
    st.subheader("🤖 EML SENTINEL AI")
    st.info("**Market:** Bullish\n**Strongest:** SPY\n**Recommendation:** Hold positions. Wait for MA crossover.")
    st.write("---")
    st.write("**CIRCUIT BREAKER:** READY")

# --- 4. TRADE JOURNAL / AUDIT LOG ---
st.subheader("📜 LIVE ACTIVITY AUDIT")
audit_data = [
    {"Time": "15:41", "Action": "BUY", "Symbol": "NVDA", "Details": "MA Crossover"},
    {"Time": "15:44", "Action": "EXIT", "Symbol": "NVDA", "Details": "TAKE PROFIT"},
    {"Time": "15:46", "Action": "BUY", "Symbol": "SPCX", "Details": "Bullish Trend"}
]
st.table(pd.DataFrame(audit_data))

# --- 5. TECHNICAL INDICATORS ---
st.subheader("📉 TECHNICAL ANALYSIS: NVDA")
tech_cols = st.columns(4)
tech_cols[0].metric("Trend", "Bullish ✅")
tech_cols[1].metric("Fast MA", "602.88")
tech_cols[2].metric("ATR", "1.82")
tech_cols[3].metric("Confidence", "94%")