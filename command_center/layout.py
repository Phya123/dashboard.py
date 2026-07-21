import streamlit as st

from command_center.panels import (
    sentinel_ai_chat,
    account_panel,
    community_panel,
    positions_panel
)

from command_center.activity import activity_panel

from ecosystem.eml_hub import eml_ecosystem_panel

from command_center.profile_panel import profile_panel


def command_center_layout(
    sentinel_state,
    account,
    community_panel,
    activity_panel,
    eml_ecosystem_panel,
    ai_panel,
    account_panel,
    sentinel_ai_chat,
    status_panel,
):

    st.title(
        "🧠 EML SENTINEL COMMAND CENTER"
    )


    st.caption(
        "🤖 SENTINEL AI CORE ONLINE | 🔒 DASHBOARD READ ONLY"
    )


    # =========================
    # AI ASSISTANT
    # =========================

    st.divider()

    sentinel_ai_chat(
        sentinel_state
    )


    # =========================
    # USER PROFILE
    # =========================

    st.divider()

    profile_panel()


    # =========================
    # ACCOUNT
    # =========================

    st.divider()

    account_panel(
        sentinel_state
    )


    


    # =========================
    # THREE PANEL SECTION
    # =========================

    st.divider()

    col1, col2, col3 = st.columns(3)


    with col1:

        community_panel(
            {
                "members": 0,
                "skills": 0,
                "opportunities": 0
            }
        )


    with col2:

        activity_panel()


    with col3:

        eml_ecosystem_panel()


    st.divider()


    st.caption(
        "EML SENTINEL IS READ ONLY — NO TRADING FUNCTIONS EXIST IN THIS DASHBOARD."
    )
