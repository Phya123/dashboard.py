import pandas as pd
import plotly.graph_objects as go


# ==========================
# CANDLESTICK CHART
# ==========================

def create_candlestick_chart(df, symbol):

    if df is None or df.empty:
        return None

    fig = go.Figure()

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
    if len(df) >= 20:
        df["MA20"] = (
            df["close"]
            .rolling(20)
            .mean()
        )

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["MA20"],
                name="MA20"
            )
        )


    # MA50
    if len(df) >= 50:
        df["MA50"] = (
            df["close"]
            .rolling(50)
            .mean()
        )

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["MA50"],
                name="MA50"
            )
        )


    fig.update_layout(
        title=f"{symbol} Market Chart",
        xaxis_title="Time",
        yaxis_title="Price",
        height=600,
        xaxis_rangeslider_visible=False
    )


    return fig



# ==========================
# VOLUME CHART
# ==========================

def create_volume_chart(df, symbol):

    if df is None or df.empty:
        return None


    fig = go.Figure()


    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["volume"],
            name="Volume"
        )
    )


    fig.update_layout(
        title=f"{symbol} Volume",
        height=300
    )


    return fig
