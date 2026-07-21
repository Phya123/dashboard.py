import streamlit as st

# =========================
# ONBOARDING IMPORT FALLBACK
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

    st.subheader("👤 Sentinel User Profile")


    profiles = load_profiles()


    # =========================
    # SENTINEL INTELLIGENCE CARD
    # =========================

    profile = sentinel_profile_summary()


    


    # =========================
    # EXISTING PROFILE
    # =========================

    if profiles:

        profile_data = profiles[0]

        st.success(
            "✅ Sentinel profile active"
        )

        st.write(
            f"Name: {profile_data.get('name','Unknown')}"
        )

        st.write(
            f"Sentinel ID: {profile_data.get('sentinel_id','N/A')}"
        )

        return



    # =========================
    # CREATE PROFILE
    # =========================

    st.info(
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


        submitted = st.form_submit_button(
            "Create Sentinel Profile"
        )


        if submitted:

            if name and sentinel_id:

                profile = {

                    "name": name,

                    "sentinel_id": sentinel_id

                }


                save_profile(profile)


                st.success(
                    "✅ Sentinel Profile Created"
                )


                st.rerun()


            else:

                st.warning(
                    "Please complete both fields."
                )
