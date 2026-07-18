import streamlit as st
from datetime import datetime


def activity_panel(events=None):

    st.divider()

    st.subheader("🔥 Sentinel Activity Stream")

    if events is None:
        events = [
            "🤖 AI Core initialized",
            "📊 Alpaca intelligence connected",
            "🌎 NeighborLink system online",
            "🚀 EML Ecosystem Hub online"
        ]

    for event in events:
        st.write(
            f"{datetime.now().strftime('%H:%M:%S')} | {event}"
        )
