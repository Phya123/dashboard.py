import plotly.graph_objects as go
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

def render_candlestick(symbol, data_client):
    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Minute,
        limit=100,
    )

    bars = data_client.get_stock_bars(request).df

    if bars.empty:
        return None

    if hasattr(bars.index, "levels"):
        bars = bars.xs(symbol)

    bars = bars.reset_index()

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=bars["timestamp"],
                open=bars["open"],
               


# ==========================
# PRICE CHART
# ==========================

def create_price_chart(df, symbol):

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


    if len(df) >= 20:

        ma20 = (
            df["close"]
            .rolling(20)
            .mean()
        )

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=ma20,
                name="MA20"
            )
        )


    if len(df) >= 50:

        ma50 = (
            df["close"]
            .rolling(50)
            .mean()
        )

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=ma50,
                name="MA50"
            )
        )


    fig.update_layout(
        title=f"{symbol} Live Market Chart",
        height=600,
        xaxis_rangeslider_visible=False
    )


    return fig



# ==========================
# CANDLESTICK ALIAS
# ==========================

def create_candlestick_chart(df, symbol):

    return create_price_chart(df, symbol)



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
