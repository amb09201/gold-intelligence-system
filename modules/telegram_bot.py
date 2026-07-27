"""
Telegram module — sends a formatted rate + recommendation alert.
"""

import requests
from datetime import datetime

from config import CONFIG
from modules.logger import log


def send_message(text):
    """Send a Markdown-formatted text message to the configured Telegram chat."""
    if not CONFIG.get("ENABLE_TELEGRAM"):
        log("Telegram disabled (ENABLE_TELEGRAM=False); skipping send.")
        return False

    if not CONFIG.get("BOT_TOKEN") or not CONFIG.get("CHAT_ID"):
        log("Telegram BOT_TOKEN or CHAT_ID missing; skipping send.", "WARNING")
        return False

    url = f"https://api.telegram.org/bot{CONFIG['BOT_TOKEN']}/sendMessage"
    payload = {
        "chat_id": CONFIG["CHAT_ID"],
        "text": text,
        "parse_mode": "Markdown",
    }

    try:
        response = requests.post(url, data=payload, timeout=15)
        response.raise_for_status()
        log("Telegram message sent.")
        return True
    except requests.RequestException as exc:
        log(f"Telegram send failed: {exc}", "ERROR")
        return False


def format_message(gold, gold_change, silver_change, recommendation):
    """Build the pretty Telegram message shown in the project spec."""
    today = datetime.now().strftime("%d %b %Y")
    currency = CONFIG["CURRENCY"]

    def fmt_change(value):
        if value > 0:
            return f"▲ {currency}{value}"
        if value < 0:
            return f"▼ {currency}{abs(value)}"
        return "— No change"

    reasons_block = "\n".join(f"✔ {r}" for r in recommendation.get("reasons", [])) or "—"

    return (
        f"🟡 *Gold Intelligence*\n"
        f"{today}\n"
        f"━━━━━━━━━━━━\n"
        f"22K Gold\n"
        f"{currency}{gold['gold22']:,}\n"
        f"{fmt_change(gold_change)}\n\n"
        f"Silver\n"
        f"{currency}{gold['silver']:,}\n"
        f"{fmt_change(silver_change)}\n"
        f"━━━━━━━━━━━━\n"
        f"Buy Score\n"
        f"{recommendation['score']}/100\n\n"
        f"Recommendation\n"
        f"{recommendation['label']}\n\n"
        f"Reasons\n"
        f"{reasons_block}\n"
        f"━━━━━━━━━━━━"
    )
