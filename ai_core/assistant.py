from scanner import get_symbol_data
from ai_core.knowledge import get_knowledge

def sentinel_response(question, state):

    if not question:
        return "Ask Sentinel a question."

    q = question.lower()


    # =========================
    # SENTINEL STATUS REPORT
    # =========================

    if (
        "status" in q
        or "system" in q
        or "report" in q
        or "what is happening" in q
    ):

        positions = state.get("positions", [])

        return f"""
🧠 SENTINEL SYSTEM REPORT


🤖 AI CORE

ONLINE


🔒 DASHBOARD

READ ONLY


📊 ALPACA INTELLIGENCE

CONNECTED


💰 EQUITY

${state.get("equity","N/A")}


💵 CASH

${state.get("cash","N/A")}


⚡ BUYING POWER

${state.get("buying_power","N/A")}


📈 POSITIONS

{len(positions)}


🌎 NEIGHBORLINK

ONLINE


🌐 EML ECOSYSTEM

ONLINE


📊 MARKET

{state.get("market_status","UNKNOWN")}


Sentinel is monitoring connected intelligence systems.
"""


    # =========================
    # EXPLAIN APP
    # =========================

    if "explain" in q or "what is this" in q:

        return """

🧠 EML SENTINEL COMMAND CENTER


Sentinel is an AI information operating system.


🤖 SENTINEL AI

Provides:

• Account intelligence
• Portfolio information
• Symbol analysis
• Market information
• Ecosystem information


📊 ALPACA INTELLIGENCE

Provides:

• Equity
• Cash
• Buying power
• Positions
• Market status


📈 MARKET TERMINAL

Displays:

• Symbol information
• Price monitoring
• Charts


🔍 SENTINEL SCANNER

Monitors tracked markets.


🌎 NEIGHBORLINK

Community intelligence system for:

• Skills
• Opportunities
• Connections


🌐 EML ECOSYSTEM HUB

Tracks:

🪙 EML Coin

🎨 NFT Collection

👟 GOAT WALKAS V2

👕 EML Clothing


🔒 SECURITY

Dashboard Mode:

READ ONLY

No trading actions happen inside this dashboard.

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
💵 Cash Available

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

    if (
        "position" in q
        or "holding" in q
        or "portfolio" in q
        or "own" in q
    ):

        positions = state.get("positions", [])

        if not positions:
            return "No open positions found."


        response = """
📊 SENTINEL POSITIONS

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

📊 Sentinel Position Report

AAPL
Shares: 0.131
Price: $326.09
P/L: +$0.93

DEO
Shares: 0.361
Price: $84.84
P/L: +$1.37

...
🧠 Portfolio Intelligence

Positions: 6
Risk: LOW
Exposure: XX%

Best performer: DEO
Worst performer: NVS

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


            if not data_client:

                data_client = state.get(
                    "alpaca_data_client"
                )


            try:

                if data_client:

                    market = get_symbol_data(
                        symbol,
                        data_client
                    )


                    if market:

                        if isinstance(market, dict):

                            price = market.get(
                                "close",
                                "Unavailable"
                            )

                        else:

                            price = market["close"]


                        price = round(
                            float(price),
                            2
                        )


            except Exception:

                price = "Unavailable"



            return f"""

📈 SENTINEL MARKET INTELLIGENCE


Symbol:

{symbol}


Current Price:

${price}


CONNECTED:

✅ Market Terminal

✅ Scanner

✅ Position Tracking


Sentinel can expand with:

• Company information
• News intelligence
• AI summaries

"""


    # =========================
    # MARKET STATUS
    # =========================

    if "market" in q:

        return f"""

📊 MARKET STATUS


{state.get("market_status","UNKNOWN")}

"""


    # =========================
    # EML ECOSYSTEM
    # =========================

    if (
        "coin" in q
        or "eml" in q
        or "goat" in q
    ):

        return """

🌐 EML ECOSYSTEM INTELLIGENCE


🪙 EML COIN

Digital ecosystem project tracking.


👟 GOAT WALKAS V2

EML footwear project.

Early ecosystem participants may receive special rewards and merchandise opportunities.


🎨 NFT COLLECTION

Digital assets connected to the ecosystem.


👕 EML BRAND

Shoes + clothing marketplace development.


"""


    # =========================
    # HELP
    # =========================

    return """

🤖 SENTINEL AI


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
