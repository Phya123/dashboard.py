import pandas as pd 
import json
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def format_currency(value):
    try: return f"${float(value):,.2f}"
    except: return "$0.00"

def format_pct(value):
    try: return f"{float(value):.2%}"
    except: return "0.00%"

def load_csv(path, columns):
    if not os.path.exists(path):
        pd.DataFrame(columns=columns).to_csv(path, index=False)
    return pd.read_csv(path)

def save_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def load_json(path):
    if not os.path.exists(path): return {}
    with open(path, 'r') as f: return json.load(f)