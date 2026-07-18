import json
import os


DATA_PATH = "data/"


def load_database(filename):

    path = os.path.join(DATA_PATH, filename)

    if not os.path.exists(path):
        return []

    try:
        with open(path, "r") as file:
            return json.load(file)

    except Exception:
        return []


def save_database(filename, data):

    path = os.path.join(DATA_PATH, filename)

    with open(path, "w") as file:
        json.dump(
            data,
            file,
            indent=4
        )
