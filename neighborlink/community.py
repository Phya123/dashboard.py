import streamlit as st




def neighborlink_panel():

    initialize_database()

    members = get_member_count()


    st.divider()

    st.subheader(
        "🌎 NeighborLink Community"
    )


    st.json({

        "status": "ONLINE",

        "members": members,

        "opportunities": 0,

        "skills_available": 0,

        "message":
        "Connecting people, skills, and opportunities."

    })
