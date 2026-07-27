"""
Telegram bot module: sends alerts and recommendations to a configured chat.
"""

import requests

import config
from modules.logger import get_logger

logger = get_logger(__name__)


def send_message(text: str) -> bool:
    """Send a plain text message via the Telegram Bot API."""
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        logger.warning("Telegram credentials not configured; skipping message send.")
        return False

    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": config.TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}

    try:
        response = requests.post(url, data=payload, timeout=15)
        response.raise_for_status()
        logger.info("Telegram message sent successfully.")
        return True
    except requests.RequestException as exc:
        logger.error(f"Failed to send Telegram message: {exc}")
        return False


def format_recommendation_message(price: float, recommendation: dict) -> str:
    """Format a recommendation dict into a readable Telegram message."""
    return (
        f"*Gold Price Update*\n"
        f"Price: ${price:,.2f}\n"
        f"Action: *{recommendation.get('action')}*\n"
        f"Confidence: {recommendation.get('confidence')}\n"
        f"Reason: {recommendation.get('reason')}"
    )
