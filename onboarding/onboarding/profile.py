import json
import os


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
