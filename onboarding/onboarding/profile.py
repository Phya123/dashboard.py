import json
import os
from datetime import datetime


PROFILE_FILE = "data/users.json"


def create_profile(name, sentinel_id):

    os.makedirs(
        "data",
        exist_ok=True
    )

    profile = {
        "name": name,
        "sentinel_id": sentinel_id,
        "created": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }


    with open(
        PROFILE_FILE,
        "w"
    ) as f:

        json.dump(
            profile,
            f,
            indent=4
        )


    return profile



def load_profiles():

    if not os.path.exists(PROFILE_FILE):

        return None


    with open(
        PROFILE_FILE,
        "r"
    ) as f:

        return json.load(f)



def get_active_profile():

    return load_profiles()
