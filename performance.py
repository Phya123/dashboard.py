import pandas as pd
import os


TRADE_FILE = "trade_journal.csv"



# ==========================
# LOAD JOURNAL
# ==========================

def load_trades():

    if not os.path.exists(
        TRADE_FILE
    ):

        return pd.DataFrame()


    try:

        df = pd.read_csv(
            TRADE_FILE
        )

        return df


    except Exception:

        return pd.DataFrame()



# ==========================
# PERFORMANCE CALCULATOR
# ==========================

def load_performance():

    df = load_trades()


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



    # Find P/L column safely

    pnl_column = None


    possible = [

        "pnl",
        "PnL",
        "profit",
        "Profit",
        "realized_pl",
        "Realized P/L"

    ]


    for col in possible:

        if col in df.columns:

            pnl_column = col
            break



    if pnl_column is None:

        df["pnl"] = 0

        pnl_column="pnl"



    df[pnl_column] = pd.to_numeric(
        df[pnl_column],
        errors="coerce"
    ).fillna(0)



    trades = len(df)



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

        (wins / trades) * 100

        if trades > 0

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


        "trades":trades,


        "wins":wins,


        "losses":losses,


        "win_rate":round(
            win_rate,
            2
        ),


        "total_pnl":round(
            float(total_pnl),
            2
        ),


        "avg_win":round(
            float(avg_win),
            2
        ),


        "avg_loss":round(
            float(avg_loss),
            2
        )

    }



# ==========================
# EQUITY CURVE DATA
# ==========================

def get_equity_curve():

    df = load_trades()


    if df.empty:

        return pd.DataFrame()



    if "pnl" not in df.columns:

        return pd.DataFrame()



    df["equity"] = (
        df["pnl"]
        .cumsum()
    )


    return df