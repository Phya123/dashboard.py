import json
import os


DATA_PATH = "data/"


def load_database(file):

    path = DATA_PATH + file

    if not os.path.exists(path):
        return []

    with open(path) as f:
        return json.load(f)


def save_database(file,data):

    with open(DATA_PATH + file,"w") as f:
        json.dump(data,f,indent=4)
