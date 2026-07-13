import os
import json
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus
from alpaca.data.historical import StockHistoricalDataClient


# ==========================
# FILES
# ==========================

TRADE_HISTORY = "alpaca_trade_history.json"

# ==========================
# COMPATIBILITY FUNCTIONS
# ==========================

def load_trade_journal():

    df = calculate_closed_trades()

    return df



def load_symbol_stats():

    return pd.DataFrame()

# ==========================
# LOAD ALPACA HISTORY
# ==========================

def load_alpaca_trades():

    try:
        load_dotenv()

        api_key = (
            os.getenv("APCA_API_KEY_ID")
            or os.getenv("ALPACA_API_KEY")
        )

        secret_key = (
            os.getenv("APCA_API_SECRET_KEY")
            or os.getenv("ALPACA_API_SECRET_KEY")
        )

        if not api_key or not secret_key:
            return pd.DataFrame()

        client = TradingClient(
            api_key,
            secret_key,
            paper=False
        )

        request = GetOrdersRequest(
            status=QueryOrderStatus.CLOSED,
            limit=500
        )

        orders = client.get_orders(
            filter=request
        )

        trades = []

        for order in orders:

            if order.filled_qty and order.filled_avg_price:

                trades.append({
                    "symbol": order.symbol,
                    "qty": float(order.filled_qty),
                    "price": float(order.filled_avg_price),
                    "side": order.side.value,
                    "executed_at": str(order.filled_at),
                    "trade_date": (
                        order.filled_at.strftime("%Y-%m-%d")
                        if order.filled_at
                        else ""
                    )
                })

        return pd.DataFrame(trades)

    except Exception as e:

        print(
            "Alpaca order history error:",
            e
        )

        return pd.DataFrame()



# ==========================
# CALCULATE CLOSED TRADE PNL
# ==========================

def calculate_closed_trades():

    df = load_alpaca_trades()

    if df.empty:
        return pd.DataFrame()

    results = []

    symbols = df["symbol"].unique()

    for symbol in symbols:

        stock = df[
            df["symbol"] == symbol
        ].sort_values(
            "executed_at"
        )


        shares = 0
        cost = 0


        for _, trade in stock.iterrows():

            qty = trade["qty"]
            price = trade["price"]


            # BUY

            if trade["side"] == "buy":

                shares += qty

                cost += qty * price



            # SELL

            elif trade["side"] == "sell":

                sell_qty = abs(qty)


                if shares > 0:


                    avg_entry = (
                        cost / shares
                    )


                    pnl = (
                        price - avg_entry
                    ) * sell_qty


                    results.append({

                        "date":
                            trade["trade_date"],

                        "symbol":
                            symbol,

                        "side":
                            "closed",

                        "qty":
                            sell_qty,

                        "entry":
                            round(
                                avg_entry,
                                4
                            ),

                        "exit":
                            price,

                        "pnl":
                            round(
                                pnl,
                                2
                            )

                    })


                    shares -= sell_qty

                    cost -= (
                        avg_entry *
                        sell_qty
                    )


    return pd.DataFrame(results)



# ==========================
# PERFORMANCE
# ==========================

def load_performance():

    df = calculate_closed_trades()


    if df.empty:

        return {

            "trades":0,
            "wins":0,
            "losses":0,
            "win_rate":0,
            "total_pnl":0,
            "avg_win":0,
            "avg_loss":0

        }



    wins = df[
        df.pnl > 0
    ]

    losses = df[
        df.pnl < 0
    ]


    return {

        "trades":
            len(df),

        "wins":
            len(wins),

        "losses":
            len(losses),

        "win_rate":
            round(
                len(wins) /
                len(df) *
                100,
                2
            ),

        "total_pnl":
            round(
                df.pnl.sum(),
                2
            ),

        "avg_win":
            round(
                wins.pnl.mean()
                if len(wins)
                else 0,
                2
            ),

        "avg_loss":
            round(
                losses.pnl.mean()
                if len(losses)
                else 0,
                2
            )

    }



# ==========================
# EQUITY CURVE
# ==========================

def get_equity_curve():

    df = calculate_closed_trades()


    if df.empty:
        return pd.DataFrame()


    df["equity"] = (
        df["pnl"]
        .cumsum()
    )


    return df
def get_open_positions():

    df = load_alpaca_trades()

    if df.empty:
        return pd.DataFrame()


    positions = []


    for symbol in df["symbol"].unique():

        stock = df[df["symbol"] == symbol]


        qty = 0
        cost = 0


        for _, trade in stock.iterrows():

            amount = float(trade["qty"])
            price = float(trade["price"])


            if trade["side"] == "buy":

                qty += amount
                cost += amount * price


            elif trade["side"] == "sell":

                sell_qty = abs(amount)

                if qty > 0:

                    avg = cost / qty

                    qty -= sell_qty
                    cost -= avg * sell_qty


        if qty > 0:

            positions.append({

                "symbol": symbol,

                "qty": round(
                    qty,
                    6
                ),

                "avg_entry": round(
                    cost / qty,
                    2
                )

            })


    return pd.DataFrame(positions)
