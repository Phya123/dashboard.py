def sentinel_response(question, state):

    if not question:
        return "Ask Sentinel a question."

    q = question.lower()


    # =========================
    # DAILY SENTINEL BRIEFING
    # =========================

    if (
        "briefing" in q
        or "daily report" in q
        or "morning report" in q
    ):

        return f"""
🧠 SENTINEL DAILY BRIEFING


🤖 AI CORE

ONLINE


🔒 DASHBOARD

READ ONLY


💰 Equity

${state.get("equity","N/A")}


💵 Cash

${state.get("cash","N/A")}


⚡ Buying Power

${state.get("buying_power","N/A")}


📈 Positions

{len(state.get("positions", []))}


🛡 Risk

{state.get("risk","UNKNOWN")}


📊 Market

{state.get("market_status","UNKNOWN")}


Sentinel is monitoring connected intelligence systems.

"""


    # =========================
    # PORTFOLIO SUMMARY
    # =========================

    if (
        "how am i doing" in q
        or "portfolio summary" in q
        or "performance" in q
    ):

        positions = state.get("positions", [])

        total_pnl = 0

        for p in positions:
            try:
                total_pnl += float(p.get("pnl", 0))
            except:
                pass


        return f"""
🧠 SENTINEL PORTFOLIO SUMMARY


💰 Equity

${state.get("equity","N/A")}


📈 Positions

{len(positions)}


📊 Unrealized P/L

${total_pnl:.2f}


🛡 Risk

{state.get("risk","UNKNOWN")}


Dashboard remains READ ONLY.

"""


    # =========================
    # POSITIONS
    # =========================

    if (
        "positions" in q
        or "holdings" in q
        or "what do i own" in q
    ):

        positions = state.get("positions", [])

        if not positions:
            return "No open positions found."


        response = """
📊 SENTINEL POSITION REPORT

"""

        for p in positions:

            response += f"""
📈 {p.get('symbol')}

Shares:
{p.get('shares')}

Price:
${p.get('price')}

P/L:
${p.get('pnl')}

"""


        return response


    # =========================
    # ACCOUNT
    # =========================

    if "equity" in q:
        return f"💰 Equity: ${state.get('equity','N/A')}"


    if "cash" in q:
        return f"💵 Cash: ${state.get('cash','N/A')}"


    if "buying power" in q:
        return f"⚡ Buying Power: ${state.get('buying_power','N/A')}"


    # =========================
    # MARKET
    # =========================

    if "market" in q:

        return f"""
📊 MARKET STATUS

{state.get("market_status","UNKNOWN")}

"""


    # =========================
    # DEFAULT
    # =========================

    return """
🤖 Ask Sentinel:

• Give me a briefing
• How am I doing?
• What positions do I own?
• What is my equity?
• What is market status?

"""
