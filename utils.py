import json
import os
from datetime import datetime


# ==========================
# FILES
# ==========================

DASHBOARD_DATA = "dashboard_data.json"



# ==========================
# SAVE DASHBOARD DATA
# ==========================

def save_dashboard_data(data):

    try:

        with open(
            DASHBOARD_DATA,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                default=str
            )

        return True


    except Exception:

        return False




# ==========================
# LOAD DASHBOARD DATA
# ==========================

def load_dashboard_data():

    if not os.path.exists(
        DASHBOARD_DATA
    ):

        return {}


    try:

        with open(
            DASHBOARD_DATA,
            "r"
        ) as f:

            return json.load(f)


    except Exception:

        return {}




# ==========================
# FORMATTING
# ==========================

def format_money(value):

    try:

        return f"${float(value):,.2f}"

    except Exception:

        return "$0.00"




def format_percent(value):

    try:

        return f"{float(value):.2f}%"

    except Exception:

        return "0.00%"




# ==========================
# TIME
# ==========================

def get_timestamp():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )




# ==========================
# SAFE NUMBER
# ==========================

def safe_float(value):

    try:

        return float(value)

    except Exception:

        return 0.0