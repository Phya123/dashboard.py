def portfolio_summary(state):

    positions = state.get("positions", [])

    total_pnl = 0
    best = None
    worst = None

    for p in positions:

        try:
            pnl = float(p.get("pnl", 0))
            total_pnl += pnl

            if best is None or pnl > best["pnl"]:
                best = {
                    "symbol": p["symbol"],
                    "pnl": pnl
                }

            if worst is None or pnl < worst["pnl"]:
                worst = {
                    "symbol": p["symbol"],
                    "pnl": pnl
                }

        except:
            pass

    return {
        "equity": state.get("equity"),
        "cash": state.get("cash"),
        "buying_power": state.get("buying_power"),
        "risk": state.get("risk"),
        "market": state.get("market_status"),
        "positions": len(positions),
        "total_pnl": round(total_pnl, 2),
        "best": best,
        "worst": worst
    }
