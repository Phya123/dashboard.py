from typing import Dict, Tuple

import pandas as pd


def load_market_data(symbols: Tuple[str, ...] = ("QQQ", "SPCX")) -> Dict[str, pd.DataFrame]:
    data: Dict[str, pd.DataFrame] = {}
    for idx, symbol in enumerate(symbols):
        dates = pd.date_range("2024-01-01", periods=30, freq="D")
        base = 100 + (len(symbol) * 3) + idx * 5
        drift = 0.7 if idx % 2 == 0 else -0.5
        prices = [base + i * 1.2 + (i % 5) * 0.4 + drift * (i + 1) for i in range(30)]
        frame = pd.DataFrame({"date": dates, "close": prices})
        frame["symbol"] = symbol
        data[symbol] = frame.set_index("date")
    return data
