from scanner import get_symbol_data


def sentinel_response(question, state):

    if not question:
        return "Ask Sentinel a question."


    q = question.lower()


    # =========================
    # SENTINEL STATUS
    # =========================

    if (
        "status" in q
        or "system" in q
        or "what is happening" in q
        or "report" in q
    ):

        positions = state.get(
            "positions",
            []
        )

        return f"""
🧠 Sentinel System Report


🤖 AI Core

ONLINE


🔒 Dashboard

READ ONLY


📊 Alpaca Intelligence

CONNECTED


💰 Account Equity

${state.get("equity","N/A")}


💵 Cash

${state.get("cash","N/A")}


⚡ Buying Power

${state.get("buying_power","N/A")}


📈 Open Positions

{len(positions)}


🌎 NeighborLink

ONLINE


🌐 EML Ecosystem

ONLINE


📊 Market

{state.get("market_status","UNKNOWN")}


Sentinel is monitoring your connected intelligence systems.
"""


    # =========================
    # EXPLAIN APP
    # =========================

    if "explain" in q or "what is this" in q:

        return """
🧠 EML SENTINEL COMMAND CENTER

EML Sentinel is an AI information command center.

🤖 Sentinel AI
Answers questions about:

• Account intelligence
• Positions
• Symbols
• Market information
• Ecosystem information


📊 Alpaca Intelligence

Provides:

• Equity
• Cash
• Buying power
• Positions
• Market status


📈 Live Market Terminal

Displays market information and charts.


🔍 Sentinel Scanner

Monitors tracked symbols.


🌎 NeighborLink

Community system for:

• Skills
• Opportunities
• Connections


🌐 EML Ecosystem Hub

Tracks:

🪙 EML Coin
🎨 NFT Collection
👟 GOAT WALKAS V2
👕 EML Clothing


🔒 Dashboard Mode:

READ ONLY

This dashboard monitors information.
It does NOT place trades.
"""


    # =========================
    # ACCOUNT
    # =========================

    if "equity" in q:

        return f"""
💰 Account Equity

${state.get("equity","N/A")}
"""


    if "cash" in q:

        return f"""
💵 Available Cash

${state.get("cash","N/A")}
"""


    if "buying power" in q:

        return f"""
⚡ Buying Power

${state.get("buying_power","N/A")}
"""


    # =========================
    # MARKET STATUS
    # =========================

    if "market status" in q or q == "market":

        return f"""
📊 Market Status

{state.get("market_status","UNKNOWN")}
"""


    # =========================
    # POSITIONS
    # =========================

    if (
        "position" in q
        or "holdings" in q
        or "own" in q
    ):

        positions = state.get(
            "positions",
            []
        )

        if not positions:

            return "No open positions found."


        response = """
📊 Sentinel Positions

"""


        for p in positions:

            if isinstance(p, dict):

                response += (
                    f"📈 {p.get('symbol')}\n"
                    f"Shares: {p.get('qty')}\n"
                    f"Price: ${p.get('current_price')}\n"
                    f"P/L: ${p.get('unrealized_pl')}\n\n"
                )

            else:

                response += (
                    f"📈 {p.symbol}\n"
                    f"Shares: {p.qty}\n"
                    f"Price: ${p.current_price}\n"
                    f"P/L: ${p.unrealized_pl}\n\n"
                )


        return response



    # =========================
    # SYMBOL INTELLIGENCE
    # =========================

    symbols = [

        "SPY",
        "QQQ",
        "NVDA",
        "AAPL",
        "MSFT",
        "AMD",
        "META",
        "AMZN",
        "GOOGL",
        "TSLA",
        "LMT",
        "XLE",
        "ASML",
        "TSM",
        "NVS",
        "SPCX",
        "DEO"

    ]


    for symbol in symbols:


        if symbol.lower() in q:


            price = "Unavailable"

            data_client = state.get(
                "data_client"
            )


            if data_client:

                try:

                    market = get_symbol_data(
                        symbol,
                        data_client
                    )


                    if market:

                        price = round(
                            float(
                                market["close"]
                            ),
                            2
                        )

                except Exception:

                    price = "Unavailable"



            response = f"""
📈 Sentinel Market Intelligence

Symbol:

{symbol}


Current Price:

${price}

"""


            positions = state.get(
                "positions",
                []
            )


            found = False


            for p in positions:


                current_symbol = (

                    p.get("symbol")

                    if isinstance(p, dict)

                    else p.symbol

                )


                if current_symbol == symbol:


                    found = True


                    response += """

💼 Your Position

"""


                    response += (

                        f"Shares: {p.get('qty') if isinstance(p,dict) else p.qty}\n"

                        f"Entry: ${p.get('avg_entry_price') if isinstance(p,dict) else p.avg_entry_price}\n"

                        f"Current: ${p.get('current_price') if isinstance(p,dict) else p.current_price}\n"

                        f"P/L: ${p.get('unrealized_pl') if isinstance(p,dict) else p.unrealized_pl}\n"

                    )


            if not found:

                response += """

You do not currently own this symbol.

"""


            response += """

✅ Market Terminal Connected
✅ Scanner Connected
✅ Position Tracking Connected


Future Modules:

• Company information
• Market news
• AI summaries

"""


            return response



    # =========================
    # EML ECOSYSTEM
    # =========================

    if (
        "coin" in q
        or "eml" in q
        or "goat" in q
    ):

        return """

🌐 EML Ecosystem Intelligence


🪙 EML Coin

Tracking ecosystem development.


👟 GOAT WALKAS V2

Upcoming EML footwear release.

Early participants will receive special ecosystem rewards and merchandise opportunities.


🎨 NFT Collection

Digital assets connected to the EML ecosystem.


👕 EML Brand

Shoes + clothing marketplace development.

"""


    # =========================
    # HELP
    # =========================

    return """
🤖 Sentinel AI

Try asking:

• Explain this app
• Give me a system report
• What is my equity?
• How much cash?
• How much buying power?
• How many positions do I have?
• What symbols do I own?
• How much is NVDA?
• How much is AAPL?
• Tell me about Tesla
• What is market status?
• Explain EML Coin
• Explain GOAT WALKAS V2
"""
