import plotly.graph_objects as go


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

    fig.update_layout(
        title=f"{symbol} Live Market Chart",
        template="plotly_dark",
        height=600,
        xaxis_rangeslider_visible=False
    )

    return fig

    except Exception as e:
        print(f"Candlestick error: {e}")
        return None
