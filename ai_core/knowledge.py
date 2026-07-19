SENTINEL_KNOWLEDGE = {

    "app": """
EML SENTINEL COMMAND CENTER

An AI information platform designed to connect:

- Account intelligence
- Market monitoring
- Community systems
- EML ecosystem projects

Dashboard mode:
READ ONLY

The dashboard displays information.
It does not place trades.
""",


    "neighborlink": """
NeighborLink is a community connection system.

Purpose:

- Connect people
- Share skills
- Discover opportunities
- Build collaboration
""",


    "eml_ecosystem": """
EML Ecosystem includes:

🪙 EML Coin

🎨 NFT Collection

👟 GOAT WALKAS V2

👕 EML Clothing

The ecosystem connects digital assets,
physical products, and community participation.
""",


    "goat_walkas": """
GOAT WALKAS V2 is an EML footwear project.

Early participants may receive special
ecosystem rewards and merchandise opportunities.
""",


    "security": """
Sentinel security principles:

- Dashboard READ ONLY
- Trading engine isolated
- Information monitoring only
- User permissions required
"""
}


def get_knowledge(topic):

    return SENTINEL_KNOWLEDGE.get(
        topic,
        "No information available."
    )
