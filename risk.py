from dataclasses import dataclass


@dataclass
class RiskProfile:
    max_position_size: float
    max_daily_loss: float
    max_drawdown: float


def get_risk_profile() -> RiskProfile:
    return RiskProfile(max_position_size=0.25, max_daily_loss=0.05, max_drawdown=0.10)
