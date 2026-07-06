import csv
from pathlib import Path
from typing import Dict, List


TRADE_FILE_PATH = Path(__file__).with_name("trade_journal.csv")
STATS_FILE_PATH = Path(__file__).with_name("symbol_stats.csv")


def ensure_trade_journal() -> None:
    if not TRADE_FILE_PATH.exists():
        with TRADE_FILE_PATH.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["symbol", "action", "price", "timestamp"])


def ensure_symbol_stats() -> None:
    if not STATS_FILE_PATH.exists():
        with STATS_FILE_PATH.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["symbol", "avg_return", "win_rate", "total_trades", "wins", "losses", "total_profit"])


def read_trade_journal() -> List[Dict[str, str]]:
    ensure_trade_journal()
    with TRADE_FILE_PATH.open("r", newline="", encoding="utf-8") as handle:
        return [
            {"symbol": row[0], "action": row[1], "price": row[2], "timestamp": row[3]}
            for row in csv.reader(handle)
            if row and row[0] != "symbol"
        ]


def read_symbol_stats() -> List[Dict[str, str]]:
    ensure_symbol_stats()
    with STATS_FILE_PATH.open("r", newline="", encoding="utf-8") as handle:
        rows: List[Dict[str, str]] = []
        for row in csv.reader(handle):
            if not row or row[0] == "symbol":
                continue

            padded_row = row + [""] * (7 - len(row))
            rows.append(
                {
                    "symbol": padded_row[0],
                    "avg_return": padded_row[1] or "0",
                    "win_rate": padded_row[2] or "0",
                    "total_trades": padded_row[3] or "0",
                    "wins": padded_row[4] or "0",
                    "losses": padded_row[5] or "0",
                    "total_profit": padded_row[6] or "0",
                }
            )
        return rows


def append_trade(symbol: str, action: str, price: str) -> None:
    ensure_trade_journal()
    with TRADE_FILE_PATH.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([symbol or "", action, price, "now"])


def get_performance_summary(trade_journal: List[Dict[str, str]]) -> Dict[str, object]:
    stats = read_symbol_stats()
    if stats:
        total_trades = sum(int(row.get("total_trades", 0)) for row in stats)
        wins = sum(int(row.get("wins", 0)) for row in stats)
        losses = sum(int(row.get("losses", 0)) for row in stats)
        total_profit = sum(float(row.get("total_profit", 0)) for row in stats)
        win_rate = wins / total_trades if total_trades else 0.0
        best_symbol = max(stats, key=lambda row: float(row.get("avg_return", 0))).get("symbol", "N/A")
    else:
        total_trades = len(trade_journal)
        wins = 0
        losses = 0
        total_profit = 0.0
        win_rate = 0.0
        best_symbol = "N/A"

    return {
        "total_trades": total_trades,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "total_profit": total_profit,
        "best_symbol": best_symbol,
    }
