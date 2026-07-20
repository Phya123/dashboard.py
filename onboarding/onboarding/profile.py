import json
import os
from datetime import datetime


PROFILE_FILE = "sentinel_profile.json"


def load_profiles():

    if not os.path.exists(PROFILE_FILE):
        return None

    with open(PROFILE_FILE, "r") as file:
        return json.load(file)


def save_profile(profile):

    with open(PROFILE_FILE, "w") as file:
        json.dump(
            profile,
            file,
            indent=4
        )


def create_profile(name, sentinel_id):

    profile = {
        "name": name,
        "sentinel_id": sentinel_id,
        "created": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "preferences": {
            "theme": "dark",
            "notifications": True
        }
    }

    save_profile(profile)

    return profile
