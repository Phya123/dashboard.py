# ============================================================
# ALPACA CLIENTS
# ============================================================

if not API_KEY or not SECRET_KEY:
    raise RuntimeError(
        "Missing Alpaca API credentials. "
        "Check ALPACA_API_KEY and ALPACA_SECRET_KEY in your .env or Streamlit secrets."
    )


@st.cache_resource
def get_trading_client():

    return TradingClient(
        api_key=API_KEY,
        secret_key=SECRET_KEY,
        paper=PAPER
    )


data_client = StockHistoricalDataClient(
    api_key=API_KEY,
    secret_key=SECRET_KEY
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

PAPER = os.getenv(
    "ALPACA_PAPER",
    "true"
).lower() == "true"





# ============================================================
# ACCOUNT PERFORMANCE
# ============================================================

def get_account_performance():

    try:

        account = trading_client.get_account()


        data = {
            "Equity": float(account.equity),
            "Cash": float(account.cash),
            "Buying Power": float(account.buying_power),
            "Portfolio Value": float(account.portfolio_value),
            "Daily P/L": float(account.equity)
            - float(account.last_equity),

            "Status": account.status,
        }


        return pd.DataFrame(
            [data]
        )


    except Exception as e:

        return pd.DataFrame(
            [{
                "Error": str(e)
            }]
        )



# ============================================================
# OPEN POSITIONS
# ============================================================

def get_open_positions():

    try:

        positions = trading_client.get_all_positions()


        rows = []


        for p in positions:

            rows.append({

                "Symbol":
                    p.symbol,

                "Qty":
                    float(p.qty),

                "Avg Entry":
                    float(p.avg_entry_price),

                "Current Price":
                    float(p.current_price),

                "Market Value":
                    float(p.market_value),

                "Unrealized P/L":
                    float(p.unrealized_pl),

                "Unrealized %":
                    float(p.unrealized_plpc) * 100

            })


        if not rows:

            return pd.DataFrame(
                columns=[
                    "Symbol",
                    "Qty",
                    "Avg Entry",
                    "Current Price",
                    "Market Value",
                    "Unrealized P/L",
                    "Unrealized %"
                ]
            )


        return pd.DataFrame(rows)


    except Exception:

        return pd.DataFrame()



# ============================================================
# CLOSED TRADES
# Reconstructed from Alpaca filled orders
# ============================================================

def get_closed_trades():

    try:

        request = GetOrdersRequest(
            status=QueryOrderStatus.CLOSED,
            limit=500
        )


        orders = trading_client.get_orders(
            filter=request
        )


        rows = []


        for order in orders:


            if order.filled_at is None:
                continue


            rows.append({

                "Symbol":
                    order.symbol,

                "Side":
                    str(order.side),

                "Qty":
                    float(
                        order.filled_qty or 0
                    ),

                "Filled Price":
                    float(
                        order.filled_avg_price or 0
                    ),

                "Status":
                    str(order.status),

                "Filled Time":
                    order.filled_at

            })


        if not rows:

            return pd.DataFrame(
                columns=[
                    "Symbol",
                    "Side",
                    "Qty",
                    "Filled Price",
                    "Status",
                    "Filled Time"
                ]
            )


        df = pd.DataFrame(rows)


        df["Filled Time"] = pd.to_datetime(
            df["Filled Time"]
        )


        return df.sort_values(
            "Filled Time",
            ascending=False
        )


    except Exception:

        return pd.DataFrame()



# ============================================================
# SYMBOL STATISTICS
# ============================================================

def get_symbol_statistics():

    try:

        trades = get_closed_trades()


        if trades.empty:

            return pd.DataFrame(
                columns=[
                    "Symbol",
                    "Trades"
                ]
            )


        stats = (
            trades
            .groupby("Symbol")
            .agg(
                Trades=("Symbol","count"),
                Volume=("Qty","sum"),
                Avg_Price=("Filled Price","mean")
            )
            .reset_index()
        )


        return stats


    except Exception:

        return pd.DataFrame()



# ============================================================
# REAL ALPACA EQUITY CURVE
# ============================================================

def get_equity_curve(days=30):

    try:

        from alpaca.trading.requests import (
            GetPortfolioHistoryRequest
        )


        end = datetime.utcnow()

        start = end - timedelta(
            days=days
        )


        request = GetPortfolioHistoryRequest(
            period=f"{days}D",
            timeframe="1D"
        )


        history = trading_client.get_portfolio_history(
            request
        )


        if history is None:
            return pd.DataFrame(
                columns=[
                    "Date",
                    "Equity"
                ]
            )


        equity = history.equity
        timestamps = history.timestamp


        rows = []


        for ts, value in zip(
            timestamps,
            equity
        ):

            rows.append({

                "Date":
                    datetime.fromtimestamp(
                        ts
                    ),

                "Equity":
                    float(value)

            })


        df = pd.DataFrame(rows)


        if not df.empty:

            df = df.sort_values(
                "Date"
            )


        return df



    except Exception as e:


        return pd.DataFrame(
            [{
                "Error": str(e)
            }]
        )



# ============================================================
# PERFORMANCE SUMMARY
# ============================================================

def get_performance_summary():

    try:

        trades = get_closed_trades()


        summary = {

            "Trades":
                len(trades),

            "Wins":
                0,

            "Losses":
                0,

            "Win Rate":
                0

        }


        return summary


    except Exception:

        return {}
