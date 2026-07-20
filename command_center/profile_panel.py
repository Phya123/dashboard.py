import streamlit as st

from onboarding.profile import load_profiles



def profile_panel():

    st.subheader(
        "👤 Sentinel User Profile"
    )


    profiles = load_profiles()


    if not profiles:

        st.info(
            "No Sentinel profile created yet."
        )

        return


    user = profiles[-1]


    st.write(
        f"Name: {user.get('name','N/A')}"
    )


    st.write(
        f"Username: {user.get('username','N/A')}"
    )


    st.write(
        "Interests:"
    )


    for item in user.get(
        "interests",
        []
    ):

        st.write(
            f"- {item}"
        )


    st.write(
        "Goals:"
    )


    for goal in user.get(
        "goals",
        []
    ):

        st.write(
            f"- {goal}"
        )


    st.divider()


    st.caption(
        "🧠 Sentinel personalization active"
    )
