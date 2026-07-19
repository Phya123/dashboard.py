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

EML Sentinel is an AI information command center.

🤖 Sentinel AI
Answers questions about your account, positions, market data, and the app.

📊 Alpaca Intelligence
Provides account information, equity, cash, buying power, positions, and market status.

📈 Live Market Terminal
Displays charts and market information for tracked symbols.

🔍 Sentinel Scanner
Analyzes your watchlist.

🌎 NeighborLink
A human connection platform for skills, opportunities, and community.

🌐 EML Ecosystem Hub
Tracks:
🪙 EML Coin
🎨 NFT Collection
👟 EML Brand

🔒 Security Rule:
This dashboard is READ ONLY.
It does not place trades.
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
    # POSITIONS
    # =========================

    if "position" in q or "hold" in q or "own" in q:

        positions = state.get("positions", [])

        if not positions:
            return "No open positions found."

        response = "📊 Current Sentinel Positions\n\n"

        for p in positions:

            if isinstance(p, dict):

                response += (
                    f"📈 {p.get('symbol','UNKNOWN')}\n"
                    f"Shares: {p.get('qty','N/A')}\n"
                    f"Current Price: ${p.get('current_price','N/A')}\n"
                    f"Unrealized P/L: ${p.get('unrealized_pl','N/A')}\n\n"
                )

            else:

                response += (
                    f"📈 {p.symbol}\n"
                    f"Shares: {p.qty}\n"
                    f"Current Price: ${p.current_price}\n"
                    f"Unrealized P/L: ${p.unrealized_pl}\n\n"
                )


        return response


    # =========================
    # MARKET STATUS
    # =========================

    if "market" in q:

        return f"""
📊 Market Status

{state.get("market_status","UNKNOWN")}
"""


    # =========================
    # SYMBOL SEARCH
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

            return f"""
📈 Sentinel Symbol Intelligence

Symbol: {symbol}

I can provide:
• Current price
• Position information
• Market status
• Recent news (when connected)
• Company information

Live symbol data connection is active through Sentinel.
"""


    # =========================
    # HELP MENU
    # =========================

    return """
🤖 Sentinel AI Commands

Try asking:

• Explain this app
• What is my equity?
• How much cash do I have?
• How much buying power?
• How many positions do I have?
• What symbols do I own?
• What is market status?
• Tell me about NVDA
• Tell me about SPY
• Explain NeighborLink
"""
