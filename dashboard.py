import streamlit as st
import os
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
import utils, scanner, performance, charts

st.set_page_config(layout="wide", page_title="EML-SENTINEL")

# Credentials
API_KEY = os.getenv("APCA_API_KEY_ID")
API_SECRET = os.getenv("APCA_API_SECRET_KEY")

if not API_KEY or not API_SECRET:
    st.error("Missing API Credentials. Check .env")
    st.stop()

# Clients
trading_client = TradingClient(API_KEY, API_SECRET, paper=False)
data_client = StockHistoricalDataClient(API_KEY, API_SECRET)

def get_data(symbol):
    req = StockBarsRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Day, start=datetime.now()-timedelta(days=365))
    return data_client.get_stock_bars(req).df

st.title("EML-SENTINEL | Live Command Center")

col1, col2, col3 = st.columns(3)

try:
    account = trading_client.get_account()
    col1.metric("Equity", utils.format_currency(account.equity))
    col2.metric("Buying Power", utils.format_currency(account.buying_power))
    col3.metric("Status", "MARKET OPEN" if account.trading_blocked == False else "BLOCKED")
except Exception as e:
    st.warning(f"Alpaca Connection Error: {e}")

# Scanner Section
st.subheader("Market Scanner")
symbols = ["LMT", "SPCX", "DEO", "NVS", "TSM", "ASML", "QQQ", "SPY", "AAPL", "XLE", "NVDA"]
scanner_results = []

for s in symbols:
    try:
        data = get_data(s)
        res = scanner.run_scanner(data)
        if res:
            res['symbol'] = s
            scanner_results.append(res)
    except: continue

st.table(pd.DataFrame(scanner_results))

# Performance
st.subheader("Trade Journal Performance")
journal = utils.load_csv("trade_journal.csv", ["date", "symbol", "pnl"])
metrics = performance.calculate_metrics(journal)
st.json(metrics)

# Refresh Logic
st.sidebar.button("Refresh Data")
st.empty()
import time; time.sleep(0.1) # Simulate logic delay