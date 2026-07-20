import streamlit as st

from onboarding.profile import create_profile


def onboarding_screen():

    st.title("🧠 Welcome to EML SENTINEL")

    st.caption(
        "Create your Sentinel identity"
    )


    name = st.text_input(
        "Your Name"
    )


    username = st.text_input(
        "Username"
    )


    st.subheader(
        "Choose your interests"
    )


    interests = []


    if st.checkbox("📊 Market Intelligence"):
        interests.append("markets")


    if st.checkbox("🌎 NeighborLink Community"):
        interests.append("community")


    if st.checkbox("🪙 EML Ecosystem"):
        interests.append("eml_ecosystem")


    if st.checkbox("👟 GOAT WALKAS V2"):
        interests.append("brand")


    if st.checkbox("🎨 NFTs"):
        interests.append("nft")


    st.subheader(
        "Your goals"
    )


    goals = []


    if st.checkbox("Learn"):
        goals.append("learning")


    if st.checkbox("Connect"):
        goals.append("networking")


    if st.checkbox("Build"):
        goals.append("building")



    if st.button(
        "🚀 Create Sentinel Profile"
    ):

        if not name or not username:

            st.warning(
                "Please enter your name and username."
            )

        else:

            profile = create_profile(
                username,
                name,
                interests,
                goals
            )


            st.success(
                "🧠 Sentinel Profile Created"
            )


            st.json(
                profile
            )
