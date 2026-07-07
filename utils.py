import json
import os
from datetime import datetime



# ==========================
# FILE PATHS
# ==========================

DATA_FILE = "dashboard_data.json"



# ==========================
# SAVE DASHBOARD DATA
# ==========================

def save_dashboard_data(data):

    try:

        with open(
            DATA_FILE,
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
        DATA_FILE
    ):

        return {}



    try:

        with open(
            DATA_FILE,
            "r"
        ) as f:

            return json.load(f)



    except Exception:

        return {}





# ==========================
# FORMAT MONEY
# ==========================

def money(value):

    try:

        return f"${float(value):,.2f}"

    except:

        return "$0.00"





# ==========================
# FORMAT PERCENT
# ==========================

def percent(value):

    try:

        return f"{float(value):.2f}%"

    except:

        return "0.00%"





# ==========================
# TIMESTAMP
# ==========================

def timestamp():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )





# ==========================
# SAFE NUMBER
# ==========================

def safe_float(value):

    try:

        return float(value)

    except:

        return 0.0