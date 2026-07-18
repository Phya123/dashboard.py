import datetime


def sentinel_response(question):

    q = question.lower()


    if "price" in q or "stock" in q or "qqq" in q:

        return (
            "I can analyze market information, but I need the "
            "live market data connection added to my AI bridge. "
            "The Market Terminal already connects to Alpaca."
        )


    if "dashboard" in q or "explain" in q:

        return """
EML SENTINEL COMMAND CENTER:

🤖 AI Core monitors your ecosystem.

💰 Account Intelligence shows Alpaca account status.

📈 Market Terminal displays price charts.

🔍 Scanner analyzes watchlist symbols.

🌎 NeighborLink connects people, skills, and opportunities.

🌐 EML Ecosystem tracks your brand, coin, and digital assets.

Dashboard mode is READ ONLY.
"""


    if "hello" in q or "hi" in q:

        return "Sentinel AI online. How can I help you understand your command center?"


    return (
        f"Sentinel received your question:\n\n"
        f"{question}\n\n"
        "I am online. More intelligence modules can be connected next."
    )
