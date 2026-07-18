import streamlit as st


def neighborlink_panel():

    st.divider()

    st.subheader("🌎 NeighborLink Community")


    st.json({

        "status": "ONLINE",

        "members": 0,

        "opportunities": 0,

        "skills_available": 0,

        "message":
        "Connecting people, skills, and opportunities."

    })
