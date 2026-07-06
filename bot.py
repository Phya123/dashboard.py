from dataclasses import dataclass
from typing import Optional


@dataclass
class BotSignal:
    command: str
    action: str
    symbol: Optional[str] = None
    detail: Optional[str] = None

    def describe(self) -> str:
        parts = [self.action]
        if self.symbol:
            parts.append(self.symbol)
        if self.detail:
            parts.append(self.detail)
        return " ".join(parts)


def parse_command(command: str) -> BotSignal:
    normalized = command.strip().upper()

    if normalized.startswith("BUY "):
        symbol = normalized.split(maxsplit=1)[1].strip()
        return BotSignal(command=command, action="BUY", symbol=symbol)

    if normalized.startswith("SELL "):
        symbol = normalized.split(maxsplit=1)[1].strip()
        return BotSignal(command=command, action="SELL", symbol=symbol)

    if normalized.startswith("EXIT"):
        detail = normalized.replace("EXIT", "", 1).strip() or "MANUAL"
        return BotSignal(command=command, action="EXIT", detail=detail)

    if normalized == "START ANALYSIS":
        return BotSignal(command=command, action="START", detail="ANALYSIS")

    if normalized == "MARKET CLOSED":
        return BotSignal(command=command, action="MARKET", detail="CLOSED")

    return BotSignal(command=command, action="UNKNOWN")
