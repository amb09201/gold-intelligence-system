"""
Gold Intelligence System — main entry point.

<<<<<<< HEAD
Pipeline:
  Joyalukkas GraphQL API
        -> should_save? -> Google Sheets (Gold_Rates)
        -> read_history -> Analytics (moving averages, trend, volatility)
        -> Recommendation (Buy Score + label + reasons)
        -> Dashboard tab update
        -> Telegram alert
=======
Orchestrates: fetch price -> log to sheet -> analyze -> recommend ->
build dashboard -> notify via Telegram.
>>>>>>> 80e5a703b5e9a10cbbb83800dbd2a9349bef8b52
"""

import sys

<<<<<<< HEAD
from modules.api import get_gold_rates
from modules.sheets import should_save, save_to_google_sheet, read_history, calculate_changes
from modules.analytics import build_analytics_summary
from modules.recommendation import build_recommendation
from modules.dashboard import update_dashboard
from modules.telegram_bot import send_message, format_message
from modules.logger import log


def run():
    log("Application started")

    # 1. Fetch live rates
    gold = get_gold_rates()

    # 2. Compute change vs last saved row (used for saving + Telegram message)
    gold_change, silver_change = calculate_changes(gold)

    # 3. Decide whether to save (duplicate detection)
    if should_save(gold):
        history_before = read_history()
        score, reasons = 0, []

        # Build a preliminary recommendation using history *before* this row,
        # so the score reflects "is NOW a good time to buy" based on the past.
        recommendation = build_recommendation(gold, history_before)

        save_to_google_sheet(
            gold,
            buy_score=recommendation["score"],
            recommendation_text=recommendation["label"],
            notes="Joyalukkas GraphQL API",
        )
        log("New prices saved")
    else:
        log("No price change detected. Skipping save.")
        history_before = read_history()
        recommendation = build_recommendation(gold, history_before)

    # 4. Analytics summary (post-save history is fine to reuse pre-save df here)
    analytics_summary = build_analytics_summary(history_before)

    # 5. Update Dashboard tab
    try:
        update_dashboard(gold, analytics_summary, recommendation)
    except Exception as exc:
        log(f"Dashboard update failed: {exc}", "ERROR")

    # 6. Telegram alert
    message = format_message(gold, gold_change, silver_change, recommendation)
    send_message(message)

    log("Application finished successfully")
=======
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
>>>>>>> 80e5a703b5e9a10cbbb83800dbd2a9349bef8b52


if __name__ == "__main__":
    try:
        run()
    except Exception as exc:
<<<<<<< HEAD
        log(str(exc), "ERROR")
=======
        logger.error(f"Run failed: {exc}")
>>>>>>> 80e5a703b5e9a10cbbb83800dbd2a9349bef8b52
        sys.exit(1)
