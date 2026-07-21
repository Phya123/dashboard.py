from scanner import get_symbol_data


def sentinel_response(question, state):

    if not question:
        return "Ask Sentinel a question."

    q = question.lower()


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

{len(state.get("positions",[]))}


🛡 Risk

{state.get("risk","UNKNOWN")}


📊 Market

{state.get("market_status","UNKNOWN")}


Sentinel is monitoring your connected intelligence systems.

"""
# =========================
# WHY DIDN'T YOU BUY?
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

Sentinel only opens a new position when ALL conditions pass:

✅ Fast MA > Slow MA

✅ Price above MA200

✅ ATR volatility filter passes

✅ Cooldown expired

✅ No existing position

✅ Market is OPEN

Current Market:
{state.get("market_status","UNKNOWN")}

Current Positions:
{len(positions)}

Risk Level:
{state.get("risk","UNKNOWN")}

This protects capital by avoiding weak or low-probability trades.

"""

📊 Market

{state.get("market_status","UNKNOWN")}


Sentinel is monitoring your connected intelligence systems.

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
        best = None
        worst = None


        for p in positions:

            try:

                pnl = float(
                    p.get("pnl",0)
                )

                total_pnl += pnl


                item = {
                    "symbol": p.get("symbol"),
                    "pnl": pnl
                }


                if best is None or pnl > best["pnl"]:
                    best = item


                if worst is None or pnl < worst["pnl"]:
                    worst = item


            except:

                pass


        return f"""

🧠 SENTINEL PORTFOLIO SUMMARY


💰 Equity

${state.get("equity","N/A")}


💵 Cash

${state.get("cash","N/A")}


⚡ Buying Power

${state.get("buying_power","N/A")}


📈 Positions

{len(positions)}


📊 Unrealized P/L

${total_pnl:.2f}


🏆 Best Position

{best["symbol"] if best else "N/A"}

${best["pnl"] if best else 0:.2f}


⚠️ Needs Attention

{worst["symbol"] if worst else "N/A"}

${worst["pnl"] if worst else 0:.2f}


🛡 Risk

{state.get("risk","UNKNOWN")}


Exposure

{state.get("exposure_percent","N/A")}%

"""


    # =========================
    # POSITION REPORT
    # =========================

    if (
        "positions" in q
        or "holdings" in q
        or "what do i own" in q
        or "stocks do i own" in q
    ):


        positions = state.get(
            "positions",
            []
        )


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
    # RISK EXPLANATION
    # =========================


    if (
        "why is my risk" in q
        or "risk" in q
    ):


        return f"""

🛡 SENTINEL RISK ANALYSIS


Current Risk:

{state.get("risk","UNKNOWN")}


Exposure:

{state.get("exposure_percent","N/A")}%


Sentinel calculates risk from:

• Account equity
• Cash available
• Market exposure
• Current holdings


Dashboard remains READ ONLY.

"""



    # =========================
    # INDIVIDUAL STOCK CHECK
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
        "DEO"
    ]


    for symbol in symbols:


        if symbol.lower() in q:


            for p in state.get("positions",[]):

                if p.get("symbol") == symbol:


                    return f"""

📈 SENTINEL HOLDING INTELLIGENCE


Symbol:

{symbol}


Shares:

{p.get('shares')}


Current Price:

${p.get('price')}


Unrealized P/L:

${p.get('pnl')}


Average Entry:

${p.get('avg_entry')}


"""



            return f"""

📈 SENTINEL MARKET INTELLIGENCE


Symbol:

{symbol}


You do not currently own this symbol.


Sentinel can monitor:

• Price
• Market data
• Scanner signals

"""



    # =========================
    # ACCOUNT QUESTIONS
    # =========================


    if "equity" in q:

        return f"💰 Equity: ${state.get('equity')}"


    if "cash" in q:

        return f"💵 Cash: ${state.get('cash')}"


    if "buying power" in q:

        return f"⚡ Buying Power: ${state.get('buying_power')}"



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
        "eml" in q
        or "coin" in q
        or "goat" in q
    ):


        return """

🌐 EML ECOSYSTEM


🪙 EML Coin

Digital ecosystem project.


👟 GOAT WALKAS V2

EML footwear project.


🎨 NFT Collection

Digital assets.


👕 EML Brand

Shoes + clothing marketplace.


"""



    # =========================
    # HELP
    # =========================


    return """

🤖 Ask Sentinel:


• Give me a briefing

• How am I doing?

• What positions do I own?

• What is my equity?

• How much cash?

• How much buying power?

• Why is my risk low?

• Tell me about AAPL

• Tell me about NVDA

• What is market status?

• Explain EML Coin

• Explain GOAT WALKAS V2


"""
