import streamlit as st


try:
    from onboarding.profile import (
        load_profiles,
        save_profile
    )

except Exception:

    def load_profiles():
        return []


    def save_profile(profile):
        return profile



def profile_panel():

    st.divider()

    st.subheader("👤 Sentinel User Profile")


    profiles = load_profiles()


    if profiles:

        profile = profiles[0]

        st.write(
            f"Name: {profile.get('name', 'Unknown')}"
        )

        st.write(
            f"Sentinel ID: {profile.get('id', 'EML-001')}"
        )


    else:

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
                "Sentinel ID",
                value="EML-001"
            )


            submitted = st.form_submit_button(
                "Create Sentinel Profile"
            )


            if submitted:

                new_profile = {

                    "name": name,

                    "id": sentinel_id

                }


                save_profile(
                    new_profile
                )


                st.success(
                    "Sentinel Profile Created"
                )


                st.rerun()
