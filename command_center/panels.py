import streamlit as st
from ai_core.assistant import sentinel_response
from ai_core.explain import explain_dashboard

def sentinel_ai_chat(state):

    st.subheader("🤖 Sentinel AI Assistant")

    question = st.text_input(
        "💬 Ask Sentinel"
    )

    if question:

        from ai_core.assistant import sentinel_response

        response = sentinel_response(
            question,
            state
        )

        st.success(response)

# =========================
# 🧠 SENTINEL HEADER
# =========================

def sentinel_header():

    st.title("🧠 EML SENTINEL COMMAND CENTER")

    st.caption(
        """
        🤖 SENTINEL AI CORE ONLINE
        
        Dashboard Mode:
        🔒 READ ONLY
        """
    )


# =========================
# 🤖 AI CORE PANEL
# =========================

def ai_panel(state):

    st.divider()

    st.subheader("🤖 EML Sentinel AI")

    st.json({
        "engine": state.get("engine", "ONLINE"),
        "market": state.get("market_status", "UNKNOWN"),
        "risk": state.get("risk", "LOW"),
        "positions": len(state.get("positions", [])),
        "message": state.get(
            "message",
            "Live Alpaca read-only intelligence connected"
        )
    })


# =========================
# 💰 ACCOUNT PANEL
# =========================

def account_panel(account):

    st.divider()

    st.subheader("💰 Account Intelligence")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Equity",
            def account_panel(account):

    equity = account.get("equity", "N/A")
    cash = account.get("cash", "N/A")
    buying_power = account.get("buying_power", "N/A")

    st.subheader("💰 Account Intelligence")

    st.metric(
        "Equity",
        f"${equity}"
    )

    st.metric(
        "Cash",
        f"${cash}"
    )

    st.metric(
        "Buying Power",
        f"${buying_power}"
    )
        )

    with col2:
        st.metric(
            "Cash",
            f"${account.cash}"
        )

    with col3:
        st.metric(
            "Buying Power",
            f"${account.buying_power}"
        )

# =========================
# 🌎 NEIGHBORLINK PANEL
# =========================

def community_panel(data):

    st.divider()

    st.subheader("🌎 NeighborLink Community")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Members", data.get("members", 0))

    with col2:
        st.metric("Skills Available", data.get("skills", 0))

    with col3:
        st.metric("Opportunities", data.get("opportunities", 0))


# =========================
# 🚀 EML ECOSYSTEM PANEL
# =========================




# =========================
# 🟢 SYSTEM STATUS
# =========================

def status_panel():

    st.divider()

    st.subheader("🧠 Sentinel Status")

    st.success(
        "EML Sentinel Command Center ONLINE"
    )

    st.info(
        "Dashboard Mode: READ ONLY"
    )
