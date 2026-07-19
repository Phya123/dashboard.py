import json
import os
from datetime import datetime


USER_FILE = "data/users.json"


def create_profile(
    username,
    name,
    interests=None,
    goals=None
):

    if interests is None:
        interests = []

    if goals is None:
        goals = []


    profile = {

        "username": username,

        "name": name,

        "created": datetime.now().isoformat(),

        "interests": interests,

        "goals": goals,

        "modules": {

            "sentinel_ai": True,

            "neighborlink": True,

            "eml_ecosystem": True,

            "market_intelligence": True

        }

    }


    save_profile(profile)


    return profile



def save_profile(profile):

    os.makedirs(
        "data",
        exist_ok=True
    )


    users = []


    if os.path.exists(USER_FILE):

        try:

            with open(
                USER_FILE,
                "r"
            ) as file:

                users = json.load(file)

        except:

            users = []


    users.append(profile)


    with open(
        USER_FILE,
        "w"
    ) as file:

        json.dump(
            users,
            file,
            indent=4
        )



def load_profiles():

    if not os.path.exists(USER_FILE):

        return []


    with open(
        USER_FILE,
        "r"
    ) as file:

        return json.load(file)
