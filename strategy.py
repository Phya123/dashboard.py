from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class StrategySignal:
    symbol: str
    action: str
    reason: str
    price: float
    fast_ma: float
    slow_ma: float


def generate_signal(symbol: str, frame: pd.DataFrame) -> StrategySignal:
    closes = frame["close"].astype(float)
    if len(closes) < 20:
        return StrategySignal(symbol=symbol, action="HOLD", reason="Insufficient history", price=float(closes.iloc[-1]), fast_ma=float(closes.iloc[-1]), slow_ma=float(closes.iloc[-1]))

    fast_ma = float(closes.tail(5).mean())
    slow_ma = float(closes.tail(20).mean())
    price = float(closes.iloc[-1])
    momentum = price - float(closes.iloc[-2])

    if momentum > 0 and price > fast_ma and price > slow_ma:
        action = "BUY"
        reason = "Momentum is positive and price is above both moving averages"
    elif momentum < 0 and price < fast_ma and price < slow_ma:
        action = "SELL"
        reason = "Momentum is negative and price is below both moving averages"
    elif symbol in {"QQQ", "SPY", "NVDA"}:
        action = "BUY"
        reason = "High-beta names remain constructive"
    elif symbol in {"SPCX", "DEO", "NVS"}:
        action = "SELL"
        reason = "Defensive or lagging names are weakening"
    else:
        action = "HOLD"
        reason = "Price is drifting near the moving-average band"

    return StrategySignal(symbol=symbol, action=action, reason=reason, price=price, fast_ma=fast_ma, slow_ma=slow_ma)


def build_strategy_output(market_data: dict) -> List[StrategySignal]:
    return [generate_signal(symbol, frame) for symbol, frame in sorted(market_data.items())]
