import json
from datetime import datetime
from ai_core.explain import explain_dashboard
from ai_core.explain import explain_dashboard


def sentinel_response(question):

    if "dashboard" in question.lower():
        return explain_dashboard()

    return f"""
Sentinel received:

{question}

AI intelligence module is online.
Advanced reasoning will connect through the Sentinel AI Core.
"""


def sentinel_response(question):

    question = question.lower()


    if "dashboard" in question or "explain" in question:
        return explain_dashboard()


    if "risk" in question:
        return (
            "Your Sentinel risk monitor shows the current "
            "risk level displayed on your dashboard."
        )


    if "position" in question:
        return (
            "Your open positions are displayed in the "
            "Open Positions panel."
        )


    return (
        "I am Sentinel AI. "
        "Ask me about your dashboard, portfolio, "
        "market terminal, or EML ecosystem."
    )

def load_state():
    with open("data/sentinel_state.json") as f:
        return json.load(f)


def sentinel_summary():

    state = load_state()

    return {
        "message":
        f"""
        Sentinel AI ONLINE.

        Market:
        {state['market']['status']}

        Equity:
        ${state['market']['equity']}

        Positions:
        {state['market']['positions']}

        Community Members:
        {state['community']['members']}

        Last Scan:
        {datetime.now()}
        """
    }
