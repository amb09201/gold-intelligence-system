"""
Gold Intelligence System — main entry point.

Orchestrates: fetch price -> log to sheet -> analyze -> recommend ->
build dashboard -> notify via Telegram.
"""

import sys

import config
from modules.api import fetch_gold_price
from modules.sheets import append_row, get_all_rows
from modules.analytics import to_dataframe, moving_averages, compute_trend, compute_volatility
from modules.recommendation import generate_recommendation
from modules.dashboard import build_dashboard
from modules.telegram_bot import send_message, format_recommendation_message
from modules.logger import get_logger
from modules.utils import utc_now_iso

logger = get_logger(__name__)


def run():
    logger.info("Starting Gold Intelligence System run...")
    config.validate_config()

    # 1. Fetch current price
    price_data = fetch_gold_price()
    price = price_data.get("price")
    timestamp = price_data.get("timestamp") or utc_now_iso()
    logger.info(f"Fetched gold price: {price} at {timestamp}")

    # 2. Log to Google Sheets
    try:
        append_row([timestamp, price])
    except Exception:
        logger.warning("Skipping sheet logging due to error (check credentials).")

    # 3. Pull historical data for analysis
    try:
        rows = get_all_rows()
    except Exception:
        logger.warning("Could not read sheet history; using empty dataset.")
        rows = []

    df = to_dataframe(rows) if rows else to_dataframe([{"timestamp": timestamp, "price": price}])
    df = moving_averages(df)

    trend = compute_trend(df)
    volatility = compute_volatility(df)
    logger.info(f"Trend: {trend}, Volatility: {volatility:.2f}")

    # 4. Generate recommendation
    recommendation = generate_recommendation(trend, volatility)
    logger.info(f"Recommendation: {recommendation}")

    # 5. Build dashboard
    try:
        build_dashboard(df, recommendation)
    except Exception as exc:
        logger.error(f"Dashboard generation failed: {exc}")

    # 6. Notify via Telegram
    message = format_recommendation_message(price or 0.0, recommendation)
    send_message(message)

    logger.info("Gold Intelligence System run complete.")


if __name__ == "__main__":
    try:
        run()
    except Exception as exc:
        logger.error(f"Run failed: {exc}")
        sys.exit(1)
