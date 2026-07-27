"""
API module: fetches gold price data from an external provider.
"""

import requests

import config
from modules.logger import get_logger

logger = get_logger(__name__)


def fetch_gold_price() -> dict:
    """
    Fetch the current gold price data.

    Returns a dict like:
        {
            "price": 2385.12,
            "currency": "USD",
            "timestamp": "2026-07-27T00:00:00+00:00"
        }
    Raises requests.RequestException on network/API failure.
    """
    headers = {"x-access-token": config.GOLD_API_KEY, "Content-Type": "application/json"}

    try:
        response = requests.get(config.GOLD_API_URL, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        return {
            "price": data.get("price"),
            "currency": "USD",
            "timestamp": data.get("timestamp"),
            "raw": data,
        }
    except requests.RequestException as exc:
        logger.error(f"Failed to fetch gold price: {exc}")
        raise


def fetch_historical_prices(days: int = 30) -> list:
    """
    Placeholder for fetching historical gold prices.
    Replace with your chosen provider's historical endpoint.
    """
    logger.warning("fetch_historical_prices is not yet implemented for a real provider.")
    return []
