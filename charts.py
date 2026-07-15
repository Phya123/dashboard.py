# ============================================================
# EML SENTINEL CHART ENGINE
# Institutional Market Terminal
# ============================================================

import plotly.graph_objects as go


def create_candlestick_chart(df, symbol):

    try:

        if df is None or df.empty:
            return None


        fig = go.Figure()


        # Candles

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


        # Volume

        if "volume" in df.columns:

            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df["volume"],
                    name="Volume",
                    yaxis="y2"
                )
            )


        fig.update_layout(

            title=f"{symbol} LIVE MARKET TERMINAL",

            template="plotly_dark",

            height=700,

            xaxis_rangeslider_visible=False,

            yaxis=dict(
                title="Price"
            ),

            yaxis2=dict(
                title="Volume",
                overlaying="y",
                side="right",
                showgrid=False
            )

        )


        return fig


    except Exception as e:

        print(
            f"Chart error {symbol}: {e}"
        )

        return None



# Keeps old dashboard calls working

def render_candlestick(df, symbol):

    return create_candlestick_chart(
        df,
        symbol
        )
