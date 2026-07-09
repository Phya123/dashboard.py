import plotly.graph_objects as go
import pandas as pd



# ==========================
# PRICE CHART
# ==========================

def create_price_chart(
    bars,
    symbol
):

    try:

        df = bars.copy()


        if df.empty:
            return None


        if "close" not in df.columns:
            return None



        # Moving averages

        df["MA20"] = (
            df["close"]
            .rolling(20)
            .mean()
        )


        df["MA50"] = (
            df["close"]
            .rolling(50)
            .mean()
        )



        fig = go.Figure()



        # Candlesticks

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



        # MA20

        fig.add_trace(

            go.Scatter(

                x=df.index,

                y=df["MA20"],

                mode="lines",

                name="MA 20"

            )

        )



        # MA50

        fig.add_trace(

            go.Scatter(

                x=df.index,

                y=df["MA50"],

                mode="lines",

                name="MA 50"

            )

        )



        fig.update_layout(

            title=f"{symbol} LIVE CHART",

            xaxis_title="Time",

            yaxis_title="Price",

            height=600,

            xaxis_rangeslider_visible=False

        )


        return fig



    except Exception:

        return None




# ==========================
# EQUITY CURVE
# ==========================

def create_equity_chart(df):


    if df.empty:

        return None



    if "equity" not in df.columns:

        return None



    fig = go.Figure()



    fig.add_trace(

        go.Scatter(

            x=df.index,

            y=df["equity"],

            mode="lines",

            name="Equity"

        )

    )



    fig.update_layout(

        title="Portfolio Growth",

        xaxis_title="Trade",

        yaxis_title="P/L",

        height=400

    )



    return fig