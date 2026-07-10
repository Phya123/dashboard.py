import os
import json
import pandas as pd


# ==========================
# FILES
# ==========================

TRADE_HISTORY = "alpaca_trade_history.json"


# ==========================
# LOAD ALPACA HISTORY
# ==========================

def load_alpaca_trades():

    if not os.path.exists(TRADE_HISTORY):
        return pd.DataFrame()

    try:
        with open(TRADE_HISTORY, "r") as f:
            data = json.load(f)

        trades = data.get(
            "trade_activities",
            []
        )

        df = pd.DataFrame(trades)

        if df.empty:
            return df


        df["qty"] = pd.to_numeric(
            df["qty"],
            errors="coerce"
        )

        df["price"] = pd.to_numeric(
            df["price"],
            errors="coerce"
        )


        return df


    except Exception as e:

        print(
            "Trade history error:",
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