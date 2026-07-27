"""
Gold Intelligence System — main entry point.

Pipeline:
  Joyalukkas GraphQL API
        -> should_save? -> Google Sheets (Gold_Rates)
        -> read_history -> Analytics (moving averages, trend, volatility)
        -> Recommendation (Buy Score + label + reasons)
        -> Dashboard tab update
        -> Telegram alert
"""

import sys

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


if __name__ == "__main__":
    try:
        run()
    except Exception as exc:
        log(str(exc), "ERROR")
        sys.exit(1)
