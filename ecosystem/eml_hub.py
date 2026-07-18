import streamlit as st


EML_COIN_LINK = "https://pump.fun/9Hiy7cj9532c4mY5Q23q9fHDQ4ANfhcDg9FpPiegpump"

NFT_LINK = (
    "https://opensea.io/item/ethereum/"
    "0x495f947276749ce646f68ac8c248420045cb7b5e/"
    "77301786922628013486301128108417173847889263236704565846500085647540693762049"
)


def eml_ecosystem_panel():

    st.divider()

    st.subheader("🌐 EML Ecosystem Hub")


    col1, col2, col3 = st.columns(3)


    with col1:

    st.metric(
        "🪙 EML Coin",
        "LIVE",
        "Tracking"
    )

    st.link_button(
        "View EML Coin",
        EML_COIN_LINK
    )

    with col2:

        st.metric(
            "🎨 NFT Collection",
            "ONLINE",
            "Digital Assets"
        )

        st.link_button(
            "View NFT Collection",
            NFT_LINK
        )


    with col3:

        st.metric(
            "👟 EML Brand",
            "ONLINE",
            "Shoes + Clothing"
        )

        st.write(
            "Marketplace coming soon"
        )
