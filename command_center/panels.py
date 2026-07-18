import streamlit as st


def ai_panel(state):

    st.divider()

    st.subheader("🤖 EML Sentinel AI")

    st.json({
        "engine": state.get("engine"),
        "market": state.get("market_status"),
        "risk": state.get("risk"),
        "positions": len(state.get("positions", [])),
        "message": state.get("message")
    })


def account_panel(account):

    st.divider()

    st.subheader("💰 Account Intelligence")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Equity",
            account.get("equity", "N/A")
        )

    with col2:
        st.metric(
            "Cash",
            account.get("cash", "N/A")
        )

    with col3:
        st.metric(
            "Buying Power",
            account.get("buying_power", "N/A")
        )


def status_panel():

    st.divider()

    st.subheader("🧠 Sentinel Status")

    st.success(
        "EML Sentinel Command Center ONLINE"
    )

    st.info(
        "Dashboard Mode: READ ONLY"
    )
