import streamlit as st



def neighborlink_panel(data):

    st.divider()

    st.subheader("🌎 NeighborLink Community")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Members",
            data.get("members",0)
        )

    with col2:
        st.metric(
            "Skills",
            data.get("skills",0)
        )

    with col3:
        st.metric(
            "Opportunities",
            data.get("opportunities",0)
        )

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
            f"${account.get('equity','N/A')}"
        )

    with col2:
        st.metric(
            "Cash",
            f"${account.get('cash','N/A')}"
        )

    with col3:
        st.metric(
            "Buying Power",
            f"${account.get('buying_power','N/A')}"
        )



# =========================
# 🌎 NEIGHBORLINK PANEL
# =========================

def community_panel(data):

    st.divider()

    st.subheader("🌎 NeighborLink Community")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Members",
            data.get("members",0)
        )

    with col2:
        st.metric(
            "Skills Available",
            data.get("skills",0)
        )

    with col3:
        st.metric(
            "Opportunities",
            data.get("opportunities",0)
        )



# =========================
# 🚀 ECOSYSTEM PANEL
# =========================

def ecosystem_panel(data):

    st.divider()

    st.subheader("🌐 EML Ecosystem Hub")

    st.write(
        {
            "🪙 EML Coin": data.get("coin","LIVE"),
            "🎨 NFT Collection": data.get("nft","ONLINE"),
            "👟 EML Brand": data.get("brand","ONLINE")
        }
    )



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
