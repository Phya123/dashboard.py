import json
from datetime import datetime


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
