import os
from datetime import datetime

import pandas as pd
import streamlit as st

from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from charts import create_price_chart
from performance import load_performance, load_trade_journal, load_symbol_stats
from scanner import run_scanner

# ==========================

# CONFIG

# ==========================

st.set_page_config(
page_title="EML SENTINEL AI COMMAND CENTER",
page_icon="🤖",
layout="wide",
)

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
"NVDA",
]

REFRESH_SECONDS = 30

# ==========================

# ENV / CONNECTION

# ==========================

API_KEY = os.getenv("APCA_API_KEY_ID") or os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("APCA_API_SECRET_KEY") or os.getenv("ALPACA_SECRET_KEY")

def _missing_keys_message() -> str:
return (
"Missing Alpaca API credentials. Set APCA_API_KEY_ID and APCA_API_SECRET_KEY "
"in your environment variables."
)

@st.cache_resource
def get_clients():
if not API_KEY or not SECRET_KEY:
return None, None

```
trading = TradingClient(
    API_KEY,
    SECRET_KEY,
    paper=False,
)

data = StockHistoricalDataClient(
    API_KEY,
    SECRET_KEY,
)

return trading, data
```

trading_client, data_client = get_clients()

if trading_client is None or data_client is None:
st.error(_missing_keys_message())
st.stop()

# ==========================

# HELPERS

# ==========================

def money(value) -> str:
try:
return f"${float(value):,.2f}"
except Exception:
return "$0.00"

def pct(value) -> str:
try:
return f"{float(value):.2f}%"
except Exception:
return "0.00%"

def safe_float(value, default=0.0) -> float:
try:
if value is None:
return default
return float(value)
except Exception:
return default

def market_status_text(clock) -> str:
try:
return "OPEN" if clock.is_open else "CLOSED"
except Exception:
return "UNKNOWN"

# ==========================

# HEADER

# ==========================

st.title("🤖 EML SENTINEL AI COMMAND CENTER")
st.caption("LIVE Alpaca Monitor | Dashboard Trading Disabled")

# ==========================

# TOP STATUS

# ==========================

try:
account = trading_client.get_account()
clock = trading_client.get_clock()

```
equity = safe_float(account.equity)
cash = safe_float(account.cash)
buying_power = safe_float(account.buying_power)
portfolio_value = safe_float(account.portfolio_value)

account_col1, account_col2, account_col3, account_col4, account_col5 = st.columns(5)

account_col1.metric("Equity", money(equity))
account_col2.metric("Cash", money(cash))
account_col3.metric("Buying Power", money(buying_power))
account_col4.metric("Portfolio Value", money(portfolio_value))
account_col5.metric("Market", market_status_text(clock))
```

except Exception as e:
st.error(f"Alpaca connection error: {e}")
st.stop()

# ==========================

# PERFORMANCE SNAPSHOT

# ==========================

perf = load_performance()

p1, p2, p3, p4, p5 = st.columns(5)
p1.metric("Trades", perf.get("trades", 0))
p2.metric("Wins", perf.get("wins", 0))
p3.metric("Losses", perf.get("losses", 0))
p4.metric("Win Rate", f'{perf.get("win_rate", 0):.2f}%')
p5.metric("Total P/L", money(perf.get("total_pnl", 0)))

st.divider()

# ==========================

# OPEN POSITIONS

# ==========================

st.subheader("📊 Open Positions")

try:
positions = trading_client.get_all_positions()

```
if positions:
    rows = []
    for p in positions:
        rows.append(
            {
                "Symbol": p.symbol,
                "Qty": safe_float(p.qty),
                "Entry": safe_float(p.avg_entry_price),
                "Current": safe_float(p.current_price),
                "Market Value": safe_float(p.market_value),
                "Unrealized P/L": safe_float(p.unrealized_pl),
                "Unrealized P/L %": safe_float(p.unrealized_plpc) * 100.0,
            }
        )

    positions_df = pd.DataFrame(rows)
    positions_df["Entry"] = positions_df["Entry"].map(money)
    positions_df["Current"] = positions_df["Current"].map(money)
    positions_df["Market Value"] = positions_df["Market Value"].map(money)
    positions_df["Unrealized P/L"] = positions_df["Unrealized P/L"].map(money)
    positions_df["Unrealized P/L %"] = positions_df["Unrealized P/L %"].map(lambda x: f"{x:.2f}%")

    st.dataframe(positions_df, use_container_width=True, hide_index=True)
else:
    st.info("No open positions.")
```

except Exception as e:
st.error(f"Positions error: {e}")

st.divider()

# ==========================

# LIVE SCANNER

# ==========================

st.subheader("🔍 Live Scanner")

try:
scan_results = run_scanner(SYMBOLS, data_client)
scan_df = pd.DataFrame(scan_results)

```
if not scan_df.empty:
    st.dataframe(scan_df, use_container_width=True, hide_index=True)
else:
    st.info("No scanner data available.")
```

except Exception as e:
st.error(f"Scanner error: {e}")

st.divider()

# ==========================

# CHARTS

# ==========================

st.subheader("📊 Market Charts")

selected_symbol = st.selectbox("Select Symbol", SYMBOLS, index=0)

try:
request = StockBarsRequest(
symbol_or_symbols=selected_symbol,
timeframe=TimeFrame.Minute,
limit=100,
)

```
bars = data_client.get_stock_bars(request).df

if not bars.empty:
    if isinstance(bars.index, pd.MultiIndex):
        bars = bars.xs(selected_symbol)

    fig = create_price_chart(bars, selected_symbol)
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Chart data unavailable.")
else:
    st.info("No market data returned for this symbol.")
```

except Exception as e:
st.error(f"Chart error: {e}")

st.divider()

# ==========================

# TRADE JOURNAL

# ==========================

st.subheader("📖 Trade Journal")

try:
journal_df = load_trade_journal()
if not journal_df.empty:
st.dataframe(journal_df, use_container_width=True, hide_index=True)
else:
st.info("No trade journal entries yet.")
except Exception as e:
st.error(f"Trade journal error: {e}")

st.divider()

# ==========================

# SYMBOL STATS

# ==========================

st.subheader("📈 Symbol Statistics")

try:
symbol_stats_df = load_symbol_stats()
if not symbol_stats_df.empty:
st.dataframe(symbol_stats_df, use_container_width=True, hide_index=True)
else:
st.info("No symbol statistics yet.")
except Exception as e:
st.error(f"Symbol stats error: {e}")

st.divider()

# ==========================

# FOOTER

# ==========================

st.write("Last Update:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
st.caption("Read-only dashboard. No order submission enabled.")
