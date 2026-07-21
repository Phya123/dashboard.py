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
    # WHY NO TRADES
    # =========================

    if (
        "why didn't you buy" in q
        or "why didnt you buy" in q
        or "why no trades" in q
        or "why no buy" in q
    ):

        positions = state.get("positions", [])

        return f"""
🧠 SENTINEL TRADE ANALYSIS


Today's market did not produce a qualified setup.


Sentinel only considers entries when conditions pass:


✅ Fast MA > Slow MA

✅ Price above MA200

✅ ATR volatility filter passes

✅ Cooldown expired

✅ No existing position

✅ Market is OPEN


📊 Market Status:

{state.get("market_status","UNKNOWN")}


📈 Current Positions:

{len(positions)}


🛡 Risk:

{state.get("risk","UNKNOWN")}


Sentinel avoids weak setups to protect capital.

"""
    # =========================
    # POSITION COUNT
    # =========================

    if (
        "how many positions" in q
        or "positions do i have" in q
    ):

        positions = state.get("positions", [])

        return f"""
📈 SENTINEL POSITIONS

Open Positions:

{len(positions)}

Dashboard remains READ ONLY.
"""


    # =========================
    # SYMBOLS OWNED
    # =========================

    if (
        "what symbols" in q
        or "what symbols do i own" in q
        or "symbols i own" in q
    ):

        positions = state.get("positions", [])

        if not positions:
            return "No open positions found."

        symbols = [
            p.get("symbol")
            for p in positions
        ]

        return f"""
📊 CURRENT HOLDINGS

{symbols}
"""


    # =========================
    # STOCK PRICE CHECK
    # =========================

    symbols = [
        "NVDA",
        "AAPL",
        "TSLA",
        "MSFT",
        "AMD",
        "META",
        "AMZN"
    ]


    for symbol in symbols:

        if symbol.lower() in q:

            price = "Unavailable"

            for p in state.get("positions", []):

                if p.get("symbol") == symbol:
                    price = p.get("price")


            return f"""
📈 SENTINEL MARKET CHECK

Symbol:

{symbol}


Current Price:

${price}


Sentinel is monitoring this asset.
"""


    # =========================
    # EML BRAND
    # =========================

    if (
        "eml coin" in q
        or "goat walkas" in q
        or "eml" in q
    ):

        return """
🌐 EML ECOSYSTEM


🪙 EML Coin

Digital ecosystem project.


👟 GOAT WALKAS V2

EML footwear brand.


👕 EML Clothing

Fashion + community.


🎨 NFT Collection

Digital assets.
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
