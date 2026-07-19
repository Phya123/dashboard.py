from datetime import datetime


def sentinel_response(question, state):

    if not question:
        return "Ask Sentinel a question."


    q = question.lower()


    # =========================
    # EXPLAIN APP
    # =========================

    if "explain" in q or "what is this" in q:

        return """
🧠 EML SENTINEL COMMAND CENTER

This application is an AI information hub.

Connected systems:

🤖 Sentinel AI
Explains account, market, and dashboard data.

📊 Alpaca Intelligence
Displays live account and market information.

🌎 NeighborLink
Community system for people, skills, and opportunities.

🌐 EML Ecosystem
Tracks EML Coin, NFTs, shoes, and clothing projects.

🔒 Dashboard Mode:
READ ONLY

This dashboard monitors information.
It does not place trades.
"""


    # =========================
    # ACCOUNT
    # =========================

    account = state.get("account")


    if account:

        if "equity" in q:

            return (
                f"Your current account equity is "
                f"${float(account.equity):,.2f}"
            )


        if "cash" in q:

            return (
                f"Your available cash is "
                f"${float(account.cash):,.2f}"
            )


        if "buying power" in q:

            return (
                f"Your buying power is "
                f"${float(account.buying_power):,.2f}"
            )


    # =========================
    # POSITIONS
    # =========================

    positions = state.get(
        "positions",
        []
    )


    if "position" in q or "hold" in q:

        if not positions:
            return "You currently have no open positions."


        response = "Current positions:\n\n"


        for p in positions:

            response += (
                f"📈 {p.get('symbol','UNKNOWN')}\n"
                f"Shares: {p.get('qty','N/A')}\n"
                f"Current Price: ${p.get('current_price','N/A')}\n"
                f"Unrealized P/L: ${p.get('unrealized_pl','0')}\n\n"
            )

            return response



    # =========================
    # MARKET
    # =========================

    if "market" in q:

        return (
            "Current market status: "
            f"{state.get('market_status','UNKNOWN')}"
        )



    # =========================
    # NEIGHBORLINK
    # =========================

    if "neighbor" in q:

        return """
🌎 NeighborLink connects people,
skills, opportunities, and projects.

Future modules:
- Profiles
- Skill marketplace
- Opportunities
- Community messaging
"""


    # =========================
    # DEFAULT
    # =========================

    return """
I am connected to Sentinel intelligence.

Try asking:

• Explain this app
• What is my equity?
• How much cash do I have?
• How many positions do I have?
• Explain NeighborLink
• What is market status?
"""
