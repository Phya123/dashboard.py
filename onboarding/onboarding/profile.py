import os
import json


PROFILE_FILE = "data/users.json"


def load_profiles():

    if not os.path.exists(PROFILE_FILE):
        return []

    try:

        with open(
            PROFILE_FILE,
            "r"
        ) as f:

            return json.load(f)

    except Exception:

        return []



def save_profile(profile):

    os.makedirs(
        "data",
        exist_ok=True
    )

    profiles = load_profiles()

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
