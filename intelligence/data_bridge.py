def build_sentinel_state(
    account,
    positions,
    market_status
):

    position_list = []

    for p in positions:
        position_list.append({
            "symbol": p.symbol,
            "qty": p.qty,
            "market_value": p.market_value,
            "unrealized_pl": p.unrealized_pl,
            "unrealized_plpc": p.unrealized_plpc
        })


# ==========================
# SENTINEL RISK ENGINE
# ==========================

equity = float(account.equity)

cash = float(account.cash)

exposure = equity - cash


if equity > 0:
    exposure_percent = (
        exposure / equity
    ) * 100
else:
    exposure_percent = 0


if exposure_percent < 30:
    risk = "LOW"

elif exposure_percent < 70:
    risk = "MODERATE"

else:
    risk = "HIGH"


state = {

    "engine": "ONLINE",

    "market_status": market_status,

    "equity": account.equity,

    "cash": account.cash,

    "buying_power": account.buying_power,

    "positions": position_list,

    "position_count": len(position_list),

    "risk": risk,

    "exposure_percent": round(
        exposure_percent,
        2
    ),

    "message": "Live Alpaca read-only intelligence connected"

}


return state
