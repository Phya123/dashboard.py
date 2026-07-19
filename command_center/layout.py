import streamlit as st


def command_center_layout(
    sentinel_state,
    account,
    community_panel,
    activity_panel,
    ecosystem_panel,
    ai_panel,
    account_panel,
    sentinel_ai_chat,
    status_panel
):

    st.title("🧠 EML SENTINEL COMMAND CENTER")

    st.caption(
        "🤖 SENTINEL AI CORE ONLINE | 🔒 DASHBOARD READ ONLY"
    )


    # =========================
    # STATUS
    # =========================

    status_panel()

    ai_panel(
    sentinel_state
    )

    sentinel_ai_chat(
    sentinel_state
    )


    # =========================
    # AI + ACCOUNT
    # =========================

    left, right = st.columns([1,1])


    with left:

        ai_panel(
            sentinel_state
        )

        sentinel_ai_chat(
            sentinel_state
        )


    with right:

        account_panel(
            account
        )


    # =========================
    # COMMUNITY / ACTIVITY / ECOSYSTEM
    # =========================

    st.divider()

    col1, col2, col3 = st.columns(3)


    with col1:

        community_panel({
            "members":0,
            "skills":0,
            "opportunities":0
        })


    with col2:

        activity_panel()


    with col3:

        ecosystem_panel()
