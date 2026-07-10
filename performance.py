import os
import json
import pandas as pd
from datetime import datetime


# ==========================
# FILES
# ==========================

TRADE_HISTORY_FILE = "alpaca_trade_history.json"
TRADE_JOURNAL_FILE = "trade_journal.csv"
SYMBOL_STATS_FILE = "symbol_stats.csv"



# ==========================
# LOAD ALPACA JSON HISTORY
# ==========================

def load_alpaca_history():

    if not os.path.exists(TRADE_HISTORY_FILE):
        return pd.DataFrame()

    try:

        with open(
            TRADE_HISTORY_FILE,
            "r"
        ) as f:

            data = json.load(f)


        trades = data.get(
            "trade_activities",
            []
        )


        if not trades:
            return pd.DataFrame()


        df = pd.DataFrame(trades)


        df["price

# ==========================
# OPEN POSITIONS
# ==========================

def get_open_positions():

    if not os.path.exists("alpaca_trade_history.json"):
        return pd.DataFrame()

    try:

        with open("alpaca_trade_history.json", "r") as f:
            data = json.load(f)


        trades = data.get("trade_activities", [])

        if not trades:
            return pd.DataFrame()


        df = pd.DataFrame(trades)


        # only buys
        buys = df[
            df["side"].str.lower() == "buy"
        ].copy()


        if buys.empty:
            return pd.DataFrame()


        buys["qty"] = buys["qty"].astype(float)
        buys["price"] = buys["price"].astype(float)


        positions = (
            buys.groupby("symbol")
            .agg(
                Qty=("qty", "sum"),
                Avg_Price=("price", "mean"),
                Invested=("gross_amount", "sum")
            )
            .reset_index()
        )


        positions.rename(
            columns={
                "symbol": "Symbol"
            },
            inplace=True
        )


        return positions


    except Exception as e:

        print(
            "Open position error:",
            e
        )

        return pd.DataFrame()