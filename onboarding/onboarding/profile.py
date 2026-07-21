import os
import json
from datetime import datetime


PROFILE_FILE = "data/users.json"


# =========================
# LOAD PROFILES
# =========================

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



# =========================
# SAVE PROFILE
# =========================

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



# =========================
# GET ACTIVE PROFILE
# =========================

def get_active_profile():

    profiles = load_profiles()

    if profiles:

        return profiles[0]

    return None



# =========================
# SENTINEL PROFILE SUMMARY
# =========================

def sentinel_profile_summary():

    profile = get_active_profile()


    if not profile:

        return {

            "user": "Not Created",

            "system":
            "EML Sentinel Command Center",

            "mode":
            "READ ONLY",

            "connected":
            [
                "Alpaca",
                "NeighborLink",
                "EML Ecosystem"
            ]

        }


    return {

        "user":
        profile.get(
            "name",
            "Unknown"
        ),

        "sentinel_id":
        profile.get(
            "sentinel_id",
            "N/A"
        ),

        "system":
        "EML Sentinel Command Center",

        "mode":
        "READ ONLY",

        "connected":
        [
            "Alpaca",
            "NeighborLink",
            "EML Ecosystem"
        ],

        "created":
        profile.get(
            "created",
            "Unknown"
        )

    }
