import plotly.graph_objects as go
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame


def render_candlestick(symbol, data_client):
    try:
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
                    high=bars["high"],
                    low=bars["low"],
                    close=bars["close"],
                    name=symbol,
                )
            ]
        )

        fig.update_layout(
            title=f"{symbol} Live Candlestick",
            xaxis_title="Time",
            yaxis_title="Price",
            xaxis_rangeslider_visible=False,
            height=500,
            margin=dict(l=10, r=10, t=40, b=10),
        )

        return fig

    except Exception as e:
        print(f"Candlestick error: {e}")
        return None
