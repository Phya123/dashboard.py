import os
import pandas as pd


# ==========================
# FILES
# ==========================

TRADE_JOURNAL = "trade_journal.csv"
SYMBOL_STATS = "symbol_stats.csv"



# ==========================
# LOAD TRADE JOURNAL
# ==========================

def load_trade_journal():

    if not os.path.exists(
        TRADE_JOURNAL
    ):
        return pd.DataFrame()


    try:

        return pd.read_csv(
            TRADE_JOURNAL
        )


    except Exception:

        return pd.DataFrame()



# ==========================
# LOAD SYMBOL STATS
# ==========================

def load_symbol_stats():

    if not os.path.exists(
        SYMBOL_STATS
    ):
        return pd.DataFrame()


    try:

        return pd.read_csv(
            SYMBOL_STATS
        )


    except Exception:

        return pd.DataFrame()



# ==========================
# PERFORMANCE CALCULATOR
# ==========================

def load_performance():

    df = load_trade_journal()


    if df.empty:

        return {

            "trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0,
            "total_pnl": 0,
            "avg_win": 0,
            "avg_loss": 0

        }



    # Find P/L column

    pnl_column = None


    possible_columns = [

        "pnl",
        "PnL",
        "profit",
        "Profit",
        "realized_pnl",
        "Realized_PnL",
        "Total_PnL"

    ]


    for col in possible_columns:

        if col in df.columns:

            pnl_column = col
            break



    if pnl_column is None:

        df["pnl"] = 0
        pnl_column = "pnl"



    df[pnl_column] = pd.to_numeric(
        df[pnl_column],
        errors="coerce"
    ).fillna(0)



    total_trades = len(df)


    wins = len(
        df[
            df[pnl_column] > 0
        ]
    )


    losses = len(
        df[
            df[pnl_column] < 0
        ]
    )



    win_rate = (

        (wins / total_trades) * 100

        if total_trades > 0

        else 0

    )



    avg_win = (

        df[df[pnl_column] > 0][pnl_column].mean()

        if wins > 0

        else 0

    )



    avg_loss = (

        df[df[pnl_column] < 0][pnl_column].mean()

        if losses > 0

        else 0

    )



    total_pnl = df[pnl_column].sum()



    return {

        "trades": total_trades,

        "wins": wins,

        "losses": losses,

        "win_rate": round(
            win_rate,
            2
        ),

        "total_pnl": round(
            float(total_pnl),
            2
        ),

        "avg_win": round(
            float(avg_win),
            2
        ),

        "avg_loss": round(
            float(avg_loss),
            2
        )

    }



# ==========================
# EQUITY CURVE DATA
# ==========================

def get_equity_curve():

    df = load_trade_journal()


    if df.empty:

        return pd.DataFrame()



    pnl_column = None


    for col in [
        "pnl",
        "PnL",
        "profit",
        "Profit"
    ]:

        if col in df.columns:

            pnl_column = col
            break



    if pnl_column is None:

        return pd.DataFrame()



    df[pnl_column] = pd.to_numeric(
        df[pnl_column],
        errors="coerce"
    ).fillna(0)



    df["equity"] = (
        df[pnl_column]
        .cumsum()
    )


    return df