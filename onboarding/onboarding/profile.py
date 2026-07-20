import json
import os

PROFILE_FILE = "sentinel_profile.json"


def load_profiles():

    if not os.path.exists(PROFILE_FILE):
        return None

    with open(PROFILE_FILE, "r") as f:
        return json.load(f)


def save_profile(profile):

    with open(PROFILE_FILE, "w") as f:
        json.dump(profile, f, indent=4)
