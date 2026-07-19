import datetime


def sentinel_response(question, state=None):

    q = question.lower()


    if "account" in q or "equity" in q or "cash" in q:

        if state:

            return f"""
💰 Account Intelligence

Equity: ${state.get('equity','N/A')}
Cash: ${state.get('cash','N/A')}
Buying Power: ${state.get('buying_power','N/A')}

Sentinel is monitoring your Alpaca account in READ ONLY mode.
"""

        return """
💰 Account Intelligence

Your dashboard is connected to Alpaca.
Account information is displayed in READ ONLY mode.
"""


    if "position" in q or "holding" in q:

        if state:

            return f"""
📊 Open Positions

Sentinel is currently tracking:
{len(state.get('positions', []))} positions.

No trading actions are performed by this dashboard.
"""

        return "Position data is connected through the Sentinel intelligence layer."


    if "market" in q:

        if state:

            return f"""
📈 Market Status

Current Market:
{state.get('market_status','UNKNOWN')}

Sentinel is monitoring market conditions.
"""

        return "Market intelligence module is online."


    if "dashboard" in q or "explain" in q:

        return """
🧠 EML SENTINEL COMMAND CENTER

This dashboard has five intelligence areas:

🤖 Sentinel AI
Explains your system status.

💰 Account Intelligence
Shows Alpaca account information.

📊 Market Terminal
Displays market charts and data.

🌎 NeighborLink
Connects people, skills, and opportunities.

🌐 EML Ecosystem
Tracks EML projects, brand, NFTs, and coin.

The dashboard is READ ONLY.
"""


    return f"""
Sentinel AI received:

"{question}"

I am online and connected to the EML SENTINEL command center.
Ask me about:
- your account
- positions
- market status
- dashboard features
- EML ecosystem
"""
