from datetime import datetime


def sentinel_response(question, state):

    q = question.lower()


    # =========================
    # APP EXPLANATION
    # =========================

    if "explain" in q and "app" in q:

        return """
EML SENTINEL is an AI command center.

It connects:
🤖 Sentinel AI Intelligence
📊 Alpaca Market Data
🌎 NeighborLink Community
🌐 EML Ecosystem

The dashboard is READ ONLY.
It monitors information and explains data.
It does not place trades.
"""


    # =========================
    # EQUITY
    # =========================

    if "equity" in q:

        account = state.get("account")

        if account:
            return f"""
Your current account equity is:

${float(account.equity):,.2f}

This represents your total account value.
"""

        return "Account data is unavailable."


    # =========================
    # CASH
    # =========================

    if "cash" in q:

        account = state.get("account")

        return f"""
Available cash:

${float(account.cash):,.2f}
"""


    # =========================
    # BUYING POWER
    # =========================

    if "buying power" in q:

        account = state.get("account")

        return f"""
Buying power:

${float(account.buying_power):,.2f}
"""


    # =========================
    # POSITIONS
    # =========================

    if "position" in q:

        positions = state.get("positions",[])

        if not positions:
            return "There are currently no positions."

        answer="Current positions:\n\n"

        for p in positions:

            answer += (
                f"{p.symbol}: "
                f"{p.qty} shares | "
                f"P/L ${p.unrealized_pl}\n"
            )

        return answer



    # =========================
    # MARKET STATUS
    # =========================

    if "market" in q:

        return f"""
Market status:

{state.get("market_status","UNKNOWN")}
"""


    # =========================
    # DEFAULT
    # =========================

    return """
I am connected to Sentinel intelligence.

Try asking:
- Explain this dashboard
- What is my equity?
- How many positions do I have?
- What is SPY price?
- Explain NeighborLink
"""
