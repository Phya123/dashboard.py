import streamlit as st

from onboarding.profile import create_profile


def onboarding_setup():

    st.subheader(
        "🚀 Sentinel Onboarding"
    )


    name = st.text_input(
        "Name"
    )


    username = st.text_input(
        "Username"
    )


    interests = st.text_area(
        "Interests"
    )


    goals = st.text_area(
        "Goals"
    )


    if st.button("Create Sentinel Profile"):

        create_profile(
            name,
            username,
            interests.split(","),
            goals.split(",")
        )


        st.success(
            "Sentinel profile created."
        )
