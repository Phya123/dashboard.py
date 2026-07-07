import plotly.graph_objects as go
import pandas as pd



# ==========================
# PRICE + MOVING AVERAGES
# ==========================

def create_price_chart(
    bars,
    symbol
):


    df = bars.copy()



    if "close" not in df.columns:

        return None



    df["FAST_MA"] = (
        df["close"]
        .rolling(20)
        .mean()
    )


    df["SLOW_MA"] = (
        df["close"]
        .rolling(50)
        .mean()
    )



    fig = go.Figure()



    # Price

    fig.add_trace(
        go.Candlestick(

            x=df.index,

            open=df["open"],

            high=df["high"],

            low=df["low"],

            close=df["close"],

            name=symbol

        )
    )



    # Fast MA

    fig.add_trace(
        go.Scatter(

            x=df.index,

            y=df["FAST_MA"],

            name="Fast MA 20"

        )
    )



    # Slow MA

    fig.add_trace(
        go.Scatter(

            x=df.index,

            y=df["SLOW_MA"],

            name="Slow MA 50"

        )
    )



    fig.update_layout(

        title=f"{symbol} Price Chart",

        xaxis_title="Time",

        yaxis_title="Price",

        height=600,

        xaxis_rangeslider_visible=False

    )


    return fig




# ==========================
# EQUITY CURVE
# ==========================

def create_equity_chart(
    df
):


    if df.empty:

        return None



    fig = go.Figure()



    fig.add_trace(

        go.Scatter(

            x=df.index,

            y=df["equity"],

            name="Account Growth"

        )

    )



    fig.update_layout(

        title="Portfolio Equity Curve",

        xaxis_title="Trade",

        yaxis_title="P/L",

        height=400

    )



    return fig