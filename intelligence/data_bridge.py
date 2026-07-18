def build_sentinel_state(
    account,
    positions,
    market_status
):

    state = {

        "engine": "ONLINE",

        "market_status": market_status,

        "equity": account.equity,

        "cash": account.cash,

        "buying_power": account.buying_power,

        "positions": [],

        "position_count": len(positions),

        "risk": "MONITORING",

        "message": "Live dashboard intelligence connected"

    }

    return state
