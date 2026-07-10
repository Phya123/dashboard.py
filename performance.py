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