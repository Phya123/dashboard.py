# ==========================
# MARKET CHARTS
# ==========================

st.divider()

st.subheader("📈 LIVE MARKET TERMINAL")


selected_symbol = st.selectbox(
    "Select Symbol",
    SYMBOLS
)


try:

    request = StockBarsRequest(
        symbol_or_symbols=[selected_symbol],
        timeframe=TimeFrame.Minute,
        limit=100
    )


    bars = data_client.get_stock_bars(request).df


    if bars is not None and not bars.empty:

        if isinstance(bars.index, pd.MultiIndex):
            bars = bars.xs(selected_symbol)


        price_chart = create_candlestick_chart(
            bars,
            selected_symbol
        )


        if price_chart:

            st.plotly_chart(
                price_chart,
                use_container_width=True
            )


        volume_chart = create_volume_chart(
            bars,
            selected_symbol
        )


        if volume_chart:

            st.plotly_chart(
                volume_chart,
                use_container_width=True
            )


    else:

        st.info(
            "No market data available. Market may be closed."
        )


except Exception as e:

    st.error(
        f"Chart Error: {e}"
                          )
