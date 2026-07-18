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


    if len(position_list) == 0:
        risk = "LOW"

    elif len(position_list) < 5:
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

        "message": "Live Alpaca read-only intelligence connected"

    }


    return state
