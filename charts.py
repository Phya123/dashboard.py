import plotly.graph_objects as go


# ============================================================
# EML SENTINEL CHART ENGINE
# ============================================================


def create_candlestick_chart(df, symbol):

    try:

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
            title=f"{symbol} LIVE MARKET",
            template="plotly_dark",
            height=600,
            xaxis_rangeslider_visible=False
        )

        return fig


    except Exception as e:

        print(
            f"Chart Error {symbol}: {e}"
        )

        return None



# ============================================================
# BACKWARD COMPATIBILITY
# Keeps older dashboard imports working
# ============================================================


def render_candlestick(df, symbol):

    return create_candlestick_chart(
        df,
        symbol
        )
