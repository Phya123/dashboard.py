import streamlit as st
from command_center.profile_panel import profile_panel

def command_center_layout(
    sentinel_state,
    account,
    community_panel,
    activity_panel,
    ecosystem_panel,
    ai_panel,
    account_panel,
    sentinel_ai_chat(sentinel_state),
    status_panel
):

    status_panel()

    st.title("🧠 EML SENTINEL COMMAND CENTER")

    st.caption(
        "🤖 SENTINEL AI CORE ONLINE | 🔒 DASHBOARD READ ONLY"
    )


    col1, col2 = st.columns([1,1])


    with col1:
        ai_panel(
            sentinel_state
        )


    with col2:
        account_panel(
            account
        )


    # AI ASSISTANT GOES HERE

st.divider()

sentinel_ai_chat(
    sentinel_state
)

ai_panel()

profile_panel()

account_panel()


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
