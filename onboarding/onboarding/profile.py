import json
import os


PROFILE_FILE = "data/users.json"


def load_profiles():

    if not os.path.exists(PROFILE_FILE):
        return []

    try:

        with open(PROFILE_FILE, "r") as f:
            return json.load(f)

    except Exception:

        return []


def create_profile(
    name,
    username,
    interests,
    goals
):

    os.makedirs(
        "data",
        exist_ok=True
    )

    profiles = load_profiles()

    profile = {
        "name": name,
        "username": username,
        "interests": interests,
        "goals": goals
    }

    profiles.append(profile)

    with open(
        PROFILE_FILE,
        "w"
    ) as f:

        json.dump(
            profiles,
            f,
            indent=4
        )

    return profile
