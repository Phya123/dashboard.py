import streamlit as st


# =========================
# PROFILE IMPORT
# =========================

try:

    from onboarding.profile import (
        load_profiles,
        save_profile,
        sentinel_profile_summary
    )

except Exception:


    def load_profiles():
        return []


    def save_profile(profile):
        return True


    def sentinel_profile_summary():

        return {
            "user": "Not Created",
            "system": "EML Sentinel Command Center",
            "mode": "READ ONLY",
            "connected": [
                "Alpaca",
                "NeighborLink",
                "EML Ecosystem"
            ]
        }



# =========================
# 👤 SENTINEL PROFILE PANEL
# =========================

def profile_panel():

    st.divider()

    st.subheader(
        "👤 Sentinel User Profile"
    )


    # =========================
    # SENTINEL IDENTITY
    # =========================

    profile = sentinel_profile_summary()


    st.info(
        f"""
🧠 Sentinel Profile


User:
{profile.get('user','Unknown')}


System:
{profile.get('system','EML Sentinel Command Center')}


Mode:
{profile.get('mode','READ ONLY')}


Connected:

✅ Alpaca

✅ NeighborLink

✅ EML Ecosystem
"""
    )


    profiles = load_profiles()



    # =========================
    # EXISTING USER
    # =========================

    if profiles:

        user = profiles[0]

        st.success(
            "✅ Sentinel profile active"
        )

        st.write(
            f"Name: {user.get('name','Unknown')}"
        )

        st.write(
            f"Sentinel ID: {user.get('sentinel_id','N/A')}"
        )

        return



    # =========================
    # CREATE PROFILE
    # =========================

    st.warning(
        "No Sentinel profile created yet."
    )


    with st.form(
        "sentinel_profile_form"
    ):

        name = st.text_input(
            "Your Name"
        )


        sentinel_id = st.text_input(
            "Sentinel ID"
        )


        create = st.form_submit_button(
            "Create Sentinel Profile"
        )


        if create:

            if name and sentinel_id:


                save_profile(
                    {
                        "name": name,
                        "sentinel_id": sentinel_id
                    }
                )


                st.success(
                    "✅ Sentinel Profile Created"
                )

                st.rerun()


            else:

                st.error(
                    "Enter your name and Sentinel ID."
                )
