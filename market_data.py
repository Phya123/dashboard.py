# ============================================================
# EML SENTINEL
# MARKET DATA ENGINE
# Centralized Alpaca Data Layer
# ============================================================

import pandas as pd

from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame


class MarketDataEngine:

    def __init__(self, data_client):

        self.data_client = data_client


    def get_bars(
        self,
        symbol,
        timeframe=TimeFrame.Minute,
        limit=200
    ):

        try:

            request = StockBarsRequest(
                symbol_or_symbols=[symbol],
                timeframe=timeframe,
                limit=limit
            )

            bars = self.data_client.get_stock_bars(request)

            df = bars.df

            # Market closed fallback
            if df.empty and timeframe == TimeFrame.Minute:

                request = StockBarsRequest(
                    symbol_or_symbols=[symbol],
                    timeframe=TimeFrame.Day,
                    limit=limit
                )

                bars = self.data_client.get_stock_bars(request)

                df = bars.df

            if df.empty:
                return None

            # Handle Alpaca MultiIndex
            if isinstance(df.index, pd.MultiIndex):

                if "symbol" in df.index.names:

                    df = df.xs(
                        symbol,
                        level="symbol"
                    )

                else:

                    df = df.xs(symbol)

            # Normalize column names
            df.columns = [str(c).lower() for c in df.columns]

            return df.sort_index()

        except Exception as e:

            print(f"[MarketDataEngine] {symbol}: {e}")

            return None
