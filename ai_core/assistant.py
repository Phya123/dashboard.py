from datetime import datetime
from scanner import get_symbol_data

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
Displays charts and market information.

🌎 NeighborLink
Community network for skills, opportunities, and connections.

🌐 EML Ecosystem Hub
Tracks:
🪙 EML Coin
🎨 NFT Collection
👟 EML Brand

🔒 Dashboard Mode:
READ ONLY
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

        response = "📊 Sentinel Positions\n\n"

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



    # Explain App

    # Account

    # Positions


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

            data_client = state.get("data_client")

            price = "Unavailable"

            if data_client:

                try:

                    market = get_symbol_data(
                        symbol,
                        data_client
                    )

                    if market:

                        price = round(
                            float(market["close"]),
                            2
                        )

                except Exception:

                    price = "Unavailable"


            response = f"""
📈 Sentinel Market Intelligence

Symbol: {symbol}

Current Price:
${price}

"""


            # Check ownership

            positions = state.get(
                "positions",
                []
            )

            for p in positions:

                if isinstance(p, dict):

                    owned = p.get("symbol")

                else:

                    owned = p.symbol


                if owned == symbol:

                    response += f"""
💼 Your Position

Shares:
{p.get('qty') if isinstance(p,dict) else p.qty}

Entry:
${p.get('avg_entry_price') if isinstance(p,dict) else p.avg_entry_price}

Current:
${p.get('current_price') if isinstance(p,dict) else p.current_price}

P/L:
${p.get('unrealized_pl') if isinstance(p,dict) else p.unrealized_pl}
"""



            response += """

✅ Position Tracking
✅ Market Terminal
✅ Scanner Monitoring

Sentinel can provide:
• Current price
• Your holdings
• Market status
• Company information
• News integration
"""


            return response

    # =========================
    # COMPANY INFORMATION
    # =========================

    companies = {
        "tesla": {
            "symbol": "TSLA",
            "name": "Tesla",
            "info": "Electric vehicle, energy storage, and AI company."
        },
        "nvda": {
            "symbol": "NVDA",
            "name": "NVIDIA",
            "info": "Semiconductor company focused on GPUs, AI chips, and data centers."
        },
        "aapl": {
            "symbol": "AAPL",
            "name": "Apple",
            "info": "Technology company known for iPhone, services, and consumer electronics."
        },
        "spy": {
            "symbol": "SPY",
            "name": "SPY ETF",
            "info": "ETF that tracks the S&P 500 index."
        },
        "qqq": {
            "symbol": "QQQ",
            "name": "QQQ ETF",
            "info": "ETF tracking the Nasdaq-100 technology-focused index."
        }
    }


    for company in companies:

        if company in q:

            data = companies[company]

            market = get_symbol_data(
                data["symbol"]
            )

            price = "Unavailable"

            if market:
                try:
                    price = round(
                        float(market["close"]),
                        2
                    )
                except:
                    pass


            return f"""
🤖 Sentinel Company Intelligence

Company:
{data["name"]}

Symbol:
{data["symbol"]}

Current Price:
${price}

Overview:
{data["info"]}

Sentinel can monitor:
✅ Price data
✅ Your position
✅ Market status
✅ Scanner information

🔒 Dashboard remains READ ONLY.
"""
        return """
🤖 Sentinel AI

Try asking:

📱 APP
• Explain this app
• What does Sentinel do?
• Explain NeighborLink
• Explain EML Ecosystem

💰 ACCOUNT
• What is my equity?
• How much cash do I have?
• How much buying power?
• How many positions do I have?
• What symbols do I own?

📈 MARKET
• What is market status?
• How much is NVDA?
• How much is AAPL?
• How much is SPY?
• How much is QQQ?
• Tell me about Tesla
• Tell me about Microsoft
• Give me market news

🌎 INTELLIGENCE
• Latest market updates
• Explain my portfolio
• Which positions are performing?
• Explain my holdings

🚀 EML ECOSYSTEM
• Tell me about EML Coin
• Tell me about GOAT WALKAS V2
• Explain the EML Brand
• Explain NFT collection
• Explain upcoming drops
• Explain airdrops and rewards

🔒 SECURITY
• Is this dashboard trading?
• What mode is Sentinel in?

Sentinel is connected to:
✅ Alpaca Intelligence
✅ Account Data
✅ Position Tracking
✅ Market Terminal
✅ Scanner Monitoring
✅ EML Ecosystem Hub

Dashboard Mode:
🔒 READ ONLY
"""


        return response


    # =========================
    # MARKET STATUS
    # =========================

    if "market" in q:

        return f"""
📊 Market Status

{state.get("market_status","UNKNOWN")}
"""


    return """
🤖 Sentinel AI

Try asking:

• Explain this app
• What is my equity?
• How much cash?
• How much buying power?
• What positions do I have?
• What symbols do I own?
• What is market status?
• Tell me about NVDA
• Tell me about SPY
"""
