"""
API module — fetches live metal rates from the Joyalukkas GraphQL endpoint.
"""

import requests

from config import CONFIG
from modules.logger import log


def get_gold_rates():
    """
    Returns today's gold/silver/platinum rates from the Joyalukkas GraphQL API.

    Returns a dict:
        {
            "rate_time": "...",
            "branch": "...",
            "gold22": int, "gold24": int, "gold18": int, "gold14": int,
            "silver": int, "platinum": int,
        }
    Raises requests.HTTPError / KeyError on failure — caller should handle.
    """
    response = requests.get(
        CONFIG["GRAPHQL_URL"],
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    response.raise_for_status()

    payload = response.json()["data"]["getgoldrates"]
    row = payload["Data"][0]

    rates = {
        "rate_time": payload["metal_rate_time"],
        "branch": row["BRANCH_NAME"],
        "gold22": int(row["GOLD_22KT_RATE"]),
        "gold24": int(row["GOLD_24KT_RATE"]),
        "gold18": int(row["GOLD_18KT_RATE"]),
        "gold14": int(row["GOLD_14KT_RATE"]),
        "silver": int(row["SILVER_RATE"]),
        "platinum": int(row["PLATINUM_RATE"]),
    }

    log(f"Fetched live rates: Gold22={rates['gold22']} Silver={rates['silver']}")
    return rates
