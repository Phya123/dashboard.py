import streamlit as st

try:
    from onboarding.profile import (
        load_profiles,
        create_profile
    )

except ModuleNotFoundError:

    def load_profiles():
        return None

    def create_profile(name, sentinel_id):
        return {
            "name": name,
            "sentinel_id": sentinel_id
        }





def profile_panel():

    st.divider()

    st.subheader("👤 Sentinel User Profile")

    profile = load_profiles()

    if profile:

        st.success("Sentinel Profile Active")

        st.write(
            f"Name: {profile.get('name')}"
        )

        st.write(
            f"Sentinel ID: {profile.get('sentinel_id')}"
        )

        st.write(
            f"Created: {profile.get('created')}"
        )

    else:

        st.info(
            "No Sentinel profile created yet."
        )

        with st.form("sentinel_profile_form"):

            name = st.text_input(
                "Your Name"
            )

                with st.form("sentinel_profile_form"):

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

            st.write("BUTTON PRESSED")

            if name and sentinel_id:

                st.write("CREATING PROFILE")

                create_profile(
                    name,
                    sentinel_id
                )

                st.success(
                    "Sentinel Profile Created"
                )

                st.rerun()

            else:

                st.warning(
                    "Please complete all fields."
                )

                if name and sentinel_id:

                    st.write("CREATING PROFILE")

                    create_profile(
                        name,
                        sentinel_id
                    )

                    st.success(
                        "Sentinel Profile Created"
                    )

                    st.rerun()

                else:

                    st.warning(
                        "Please complete all fields."
                    )

                    st.success(
                        "Sentinel Profile Created"
                    )

                    st.rerun()

                else:

                    st.warning(
                        "Please complete all fields."
                    )
