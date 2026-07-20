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



def save_profiles(profiles):

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(PROFILE_FILE, "w") as f:
        json.dump(
            profiles,
            f,
            indent=4
        )



def create_profile(
    name,
    username,
    interests=None,
    goals=None
):

    profiles = load_profiles()

    profile = {
        "name": name,
        "username": username,
        "interests": interests or [],
        "goals": goals or []
    }


    profiles.append(profile)

    save_profiles(
        profiles
    )

    return profile
