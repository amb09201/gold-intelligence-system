import requests

from config import Config


def fetch_gold_rates():

    response = requests.get(
        Config.GRAPHQL_URL,
        headers={
            "User-Agent": Config.USER_AGENT
        },
        timeout=30,
    )

    response.raise_for_status()

    payload = response.json()["data"]["getgoldrates"]

    row = payload["Data"][0]

    return {
        "rate_time": payload["metal_rate_time"],
        "gold14": int(row["GOLD_14KT_RATE"]),
        "gold18": int(row["GOLD_18KT_RATE"]),
        "gold22": int(row["GOLD_22KT_RATE"]),
        "gold24": int(row["GOLD_24KT_RATE"]),
        "silver": int(row["SILVER_RATE"]),
        "platinum": int(row["PLATINUM_RATE"]),
    }
