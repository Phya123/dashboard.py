import json
import os
import time
from pathlib import Path
from urllib import error, request

import pandas as pd
import streamlit as st

try:
    from alpaca.trading.client import TradingClient
except ImportError:  # pragma: no cover - optional dependency
    TradingClient = None

from bot import parse_command
from data import load_market_data
from performance import append_trade, get_performance_summary, read_trade_journal
from risk import get_risk_profile
from strategy import build_strategy_output

st.set_page_config(page_title="Trading Operations Dashboard", page_icon="📈", layout="wide")

# Initialize session state for persistent data storage across reruns
if "dashboard_initialized" not in st.session_state:
    st.session_state.dashboard_initialized = True
    st.session_state.bot_commands_logged = set()
    st.session_state.cached_dashboard_data = None
    st.session_state.cached_dashboard_timestamp = 0
    st.session_state.cached_market_data = None
    st.session_state.cached_market_timestamp = 0
    st.session_state.cached_risk_profile = None
    st.session_state.cached_trade_journal = None
    st.session_state.cached_performance = None


def _read_dotenv(path: Path) -> dict:
    values: dict = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("\"'")
    return values


def get_alpaca_credentials() -> tuple[str | None, str | None, str | None]:
    env = os.environ
    for key_name, secret_name, base_name in [
        ("APCA_API_KEY_ID", "APCA_API_SECRET_KEY", "APCA_API_BASE_URL"),
        ("ALPACA_API_KEY", "ALPACA_API_SECRET", "ALPACA_API_BASE_URL"),
        ("ALPACA_KEY", "ALPACA_SECRET", "ALPACA_BASE_URL"),
    ]:
        api_key = env.get(key_name)
        api_secret = env.get(secret_name)
        if api_key and api_secret:
            return api_key, api_secret, env.get(base_name, "https://paper-api.alpaca.markets")

    dotenv_values = _read_dotenv(Path(__file__).with_name(".env"))
    for key_name, secret_name, base_name in [
        ("APCA_API_KEY_ID", "APCA_API_SECRET_KEY", "APCA_API_BASE_URL"),
        ("ALPACA_API_KEY", "ALPACA_API_SECRET", "ALPACA_API_BASE_URL"),
        ("ALPACA_KEY", "ALPACA_SECRET", "ALPACA_BASE_URL"),
    ]:
        api_key = dotenv_values.get(key_name)
        api_secret = dotenv_values.get(secret_name)
        if api_key and api_secret:
            return api_key, api_secret, dotenv_values.get(base_name, "https://paper-api.alpaca.markets")

    try:
        secrets = st.secrets
    except Exception:
        secrets = {}

    if isinstance(secrets, dict):
        alpaca = secrets.get("alpaca", {})
        if isinstance(alpaca, dict):
            api_key = alpaca.get("api_key") or alpaca.get("key")
            api_secret = alpaca.get("api_secret") or alpaca.get("secret")
            base_url = alpaca.get("base_url") or "https://paper-api.alpaca.markets"
            if api_key and api_secret:
                return api_key, api_secret, base_url

    return None, None, None


def fetch_alpaca_json(endpoint: str):
    api_key, api_secret, base_url = get_alpaca_credentials()
    if not api_key or not api_secret:
        return None

    if base_url and base_url.startswith("https://api.alpaca.markets"):
        base_url = base_url.rstrip("/")
    elif base_url and base_url.startswith("https://paper-api.alpaca.markets"):
        base_url = base_url.rstrip("/")
    else:
        base_url = "https://api.alpaca.markets"

    url = f"{base_url.rstrip('/')}{endpoint}" if base_url else f"https://api.alpaca.markets{endpoint}"
    headers = {
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": api_secret,
        "Accept": "application/json",
    }

    try:
        req = request.Request(url, headers=headers, method="GET")
        with request.urlopen(req, timeout=10) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except error.HTTPError as exc:
        st.warning(f"Alpaca request failed with status {exc.code}.")
        return None
    except Exception as exc:  # pragma: no cover - defensive for runtime environments
        st.warning(f"Unable to reach Alpaca: {exc}")
        return None


def load_dashboard_data():
    """Load dashboard data with session-based caching to avoid frequent API calls."""
    current_time = time.time()
    cache_duration = 30  # Refresh every 30 seconds
    
    # Return cached data if it's still fresh
    if (st.session_state.cached_dashboard_data is not None and 
        current_time - st.session_state.cached_dashboard_timestamp < cache_duration):
        return st.session_state.cached_dashboard_data
    
    account = fetch_alpaca_json("/v2/account")
    positions = fetch_alpaca_json("/v2/positions")

    if account is None or positions is None:
        data = {
            "source": "sample",
            "account": {
                "portfolio_value": "128500",
                "buying_power": "45250",
                "equity": "128500",
                "last_equity": "120300",
            },
            "positions": [
                {"symbol": "AAPL", "qty": "15", "market_value": "5400", "unrealized_plpc": "0.012"},
                {"symbol": "MSFT", "qty": "12", "market_value": "4340", "unrealized_plpc": "0.008"},
                {"symbol": "NVDA", "qty": "8", "market_value": "2920", "unrealized_plpc": "0.016"},
            ],
        }
    else:
        data = {"source": "live", "account": account, "positions": positions}
    
    # Cache the result
    st.session_state.cached_dashboard_data = data
    st.session_state.cached_dashboard_timestamp = current_time
    
    return data


def build_sample_frame():
    dates = pd.date_range("2024-01-01", periods=30, freq="D")
    revenue = [80 + i * 1.4 + (i % 7) * 1.5 for i in range(30)]
    active_users = [180 + i * 3 + (i % 5) * 4 for i in range(30)]
    conversion = [2.4 + i * 0.02 + (i % 4) * 0.05 for i in range(30)]

    frame = pd.DataFrame(
        {
            "date": dates,
            "revenue": revenue,
            "active_users": active_users,
            "conversion_rate": conversion,
        }
    ).set_index("date")
    return frame


st.title("Trading Operations Dashboard")
st.caption("Monitor account health, exposure, and performance from one place.")

# Load or use cached data with smart refresh logic
state = load_dashboard_data()

# Cache market data with longer TTL (60 seconds) since it's less critical
current_time = time.time()
market_cache_duration = 60
if (st.session_state.cached_market_data is None or 
    current_time - st.session_state.cached_market_timestamp >= market_cache_duration):
    st.session_state.cached_market_data = load_market_data(("SPY", "QQQ", "AAPL", "LMT", "XLE", "SPCX", "NVDA", "ASML", "TSM", "DEO", "NVS"))
    st.session_state.cached_market_timestamp = current_time
else:
    st.session_state.cached_market_data = st.session_state.cached_market_data

market_data = st.session_state.cached_market_data
strategy_signals = build_strategy_output(market_data)

# Cache risk profile (relatively static, cache for 5 minutes)
risk_cache_duration = 300
if (st.session_state.cached_risk_profile is None or 
    current_time - st.session_state.get("risk_profile_timestamp", 0) >= risk_cache_duration):
    st.session_state.cached_risk_profile = get_risk_profile()
    st.session_state.risk_profile_timestamp = current_time
else:
    st.session_state.cached_risk_profile = st.session_state.cached_risk_profile

risk_profile = st.session_state.cached_risk_profile

# Cache trade journal (refresh every 60 seconds)
trade_journal_cache_duration = 60
if (st.session_state.cached_trade_journal is None or 
    current_time - st.session_state.get("trade_journal_timestamp", 0) >= trade_journal_cache_duration):
    st.session_state.cached_trade_journal = read_trade_journal()
    st.session_state.trade_journal_timestamp = current_time
else:
    st.session_state.cached_trade_journal = st.session_state.cached_trade_journal

trade_journal = st.session_state.cached_trade_journal

# Cache performance summary (refresh with trade journal, 60 seconds)
if (st.session_state.cached_performance is None or 
    current_time - st.session_state.get("trade_journal_timestamp", 0) >= trade_journal_cache_duration):
    st.session_state.cached_performance = get_performance_summary(trade_journal)
else:
    st.session_state.cached_performance = st.session_state.cached_performance

performance_summary = st.session_state.cached_performance

sample_commands = [
    "BUY QQQ",
    "SELL SPCX",
    "EXIT TAKE PROFIT",
    "START ANALYSIS",
    "MARKET CLOSED",
]

parsed_commands = [parse_command(command) for command in sample_commands]

with st.sidebar:
    st.subheader("Bot Commands")
    # Disabled placeholder button that preserves the UI without allowing execution.
    st.button("BUY QQQ", disabled=True)

    for signal in parsed_commands:
        st.write(f"{signal.action}: {signal.describe()}")
        if signal.action in {"BUY", "SELL", "EXIT"}:
            symbol = signal.symbol or ""
            entry_key = (signal.action, symbol, signal.detail or "0")
            if entry_key not in st.session_state.bot_commands_logged:
                append_trade(symbol, signal.action, signal.detail or "0")
                st.session_state.bot_commands_logged.add(entry_key)

    st.subheader("Risk Profile")
    st.write(f"Max position size: {risk_profile.max_position_size:.0%}")
    st.write(f"Max daily loss: {risk_profile.max_daily_loss:.0%}")
    st.write(f"Max drawdown: {risk_profile.max_drawdown:.0%}")


if state["source"] == "live":
    st.success("Connected to Alpaca and pulling live account data.")
else:
    st.info("Alpaca credentials were not found, so sample values are being displayed.")

account = state["account"]
positions = state["positions"]

portfolio_value = float(account.get("portfolio_value", 0) or 0)
buying_power = float(account.get("buying_power", 0) or 0)
cash = float(account.get("cash", 0) or 0)
last_equity = float(account.get("last_equity", portfolio_value) or portfolio_value)
current_equity = float(account.get("equity", portfolio_value) or portfolio_value)
daily_pnl = current_equity - last_equity

positions_df = pd.DataFrame(positions)
if not positions_df.empty:
    positions_df["qty"] = pd.to_numeric(positions_df.get("qty", 0), errors="coerce").fillna(0)
    positions_df["market_value"] = pd.to_numeric(positions_df.get("market_value", 0), errors="coerce").fillna(0)
    positions_df["unrealized_plpc"] = pd.to_numeric(positions_df.get("unrealized_plpc", 0), errors="coerce").fillna(0)
    positions_df["current_price"] = positions_df["market_value"] / positions_df["qty"].replace(0, pd.NA)
    positions_df["entry_price"] = positions_df["current_price"] / (1 + positions_df["unrealized_plpc"]).replace(0, pd.NA)
    positions_df["unrealized_pnl"] = (positions_df["current_price"] - positions_df["entry_price"]) * positions_df["qty"]
    positions_df = positions_df[["symbol", "qty", "entry_price", "current_price", "unrealized_pnl"]].sort_values("unrealized_pnl", ascending=False)

st.subheader("Account")
account_cols = st.columns(4)
with account_cols[0]:
    st.metric("Live account value", f"${portfolio_value:,.0f}")
with account_cols[1]:
    st.metric("Buying power", f"${buying_power:,.0f}")
with account_cols[2]:
    st.metric("Cash", f"${cash:,.0f}")
with account_cols[3]:
    st.metric("Today's P&L", f"${daily_pnl:,.0f}")

st.subheader("Market Status")
status_cols = st.columns(6)
with status_cols[0]:
    st.metric("Market Status", "🟢 OPEN")
with status_cols[1]:
    st.metric("Buying Power", "$96.00")
with status_cols[2]:
    st.metric("Cash Used", "84%")
with status_cols[3]:
    st.metric("Open Positions", len(positions_df))
with status_cols[4]:
    st.metric("Risk", "LOW")
with status_cols[5]:
    st.metric("Today's Drawdown", "0.12%")

st.metric("Circuit Breaker", "READY")

st.subheader("EML Sentinel AI")
st.info(
    "Current Market: Bullish\n"
    "Strongest Symbol: NVDA\n"
    "Weakest Symbol: QQQ\n"
    "Cash Available: $96\n"
    "Recommendation: Wait for MA crossover. No high-confidence trades."
)

st.divider()

st.subheader("Open Positions")
if not positions_df.empty:
    st.dataframe(positions_df, use_container_width=True)
else:
    st.info("No open positions to display yet.")

st.divider()

st.subheader("Watchlist")
watchlist_rows = []
for signal in strategy_signals:
    if signal.action == "BUY":
        direction = "Bullish"
        trend = "Uptrend"
    elif signal.action == "SELL":
        direction = "Bearish"
        trend = "Downtrend"
    else:
        direction = "Neutral"
        trend = "Sideways"

    watchlist_rows.append(
        {
            "Symbol": signal.symbol,
            "Sentiment": direction,
            "Last price": f"${signal.price:,.2f}",
            "Current trend": trend,
        }
    )

st.dataframe(pd.DataFrame(watchlist_rows), use_container_width=True)

st.divider()

st.subheader("Performance")
performance_cols = st.columns(6)
with performance_cols[0]:
    st.metric("Total trades", performance_summary["total_trades"])
with performance_cols[1]:
    st.metric("Wins", performance_summary["wins"])
with performance_cols[2]:
    st.metric("Losses", performance_summary["losses"])
with performance_cols[3]:
    st.metric("Win rate", f"{performance_summary['win_rate']:.0%}")
with performance_cols[4]:
    st.metric("Total profit", f"${performance_summary['total_profit']:,.0f}")
with performance_cols[5]:
    st.metric("Best-performing symbol", performance_summary["best_symbol"])

st.divider()

st.subheader("Live Activity")
api_key, api_secret, _ = get_alpaca_credentials()
if TradingClient is not None and api_key and api_secret:
    client = TradingClient(api_key, api_secret, paper=True)
    orders = client.get_orders(status="all", limit=10)
    order_rows = [
        {
            "Symbol": getattr(order, "symbol", ""),
            "Side": getattr(order, "side", ""),
            "Status": getattr(order, "status", ""),
            "Filled": getattr(order, "filled_qty", ""),
        }
        for order in orders
    ]
    if order_rows:
        st.dataframe(pd.DataFrame(order_rows), use_container_width=True)
    else:
        st.info("No recent orders found.")
else:
    live_activity_data = []
    for entry in trade_journal[-20:]:
        symbol = entry.get("symbol") or entry.get("Symbol") or ""
        action = entry.get("action") or entry.get("Action") or "UNKNOWN"
        price = entry.get("price") or entry.get("Price") or "0"
        timestamp = entry.get("timestamp") or entry.get("Timestamp") or ""
        live_activity_data.append(
            {
                "Symbol": symbol or "—",
                "Action": action,
                "Price": price,
                "Timestamp": timestamp,
            }
        )

    activity_df = pd.DataFrame(live_activity_data).copy()
    if not activity_df.empty:
        activity_df = activity_df.reset_index(drop=True)
        st.dataframe(activity_df, use_container_width=True)
    else:
        st.info("No live activity recorded yet.")

with st.expander("Connection setup"):
    st.write("Set these environment variables before running the app to use live Alpaca data:")
    st.code(
        "export APCA_API_KEY_ID=your_key\n"
        "export APCA_API_SECRET_KEY=your_secret\n"
        "export APCA_API_BASE_URL=https://paper-api.alpaca.markets"
    )
