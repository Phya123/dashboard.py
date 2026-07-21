import json
import os


PROFILE_FILE = "data/profile.json"


def load_profile():

    if not os.path.exists(PROFILE_FILE):
        return None

    with open(PROFILE_FILE, "r") as f:
        return json.load(f)



def save_profile(profile):

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(PROFILE_FILE, "w") as f:
        json.dump(
            profile,
            f,
            indent=4
        )



def create_profile(
    name,
    sentinel_id
):

    profile = {

        "name": name,

        "sentinel_id": sentinel_id

    }


    save_profile(profile)

    return profile
