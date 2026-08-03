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

#from config import CONFIG
from modules.api import get_gold_rates
from modules.sheets import should_save, save_to_google_sheet, read_history, calculate_changes
from modules.analytics import build_analytics_summary
from modules.recommendation import build_recommendation
from modules.dashboard import update_dashboard
from modules.telegram_bot import send_message, format_message
from modules.settings import apply_settings
from modules.users import load_users
from modules.logger import log


def run():
    log("Application started")

    # 0. Load overrides from the "Settings" sheet tab (BUY_TARGET, ENABLE_TELEGRAM, etc.)
    apply_settings()

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

    # 6. Telegram alerts — one per user in the "Users" sheet tab, each scored
    # against their own BuyTarget. Falls back to single-user CONFIG if no
    # "Users" tab exists. Alerts are ONLY sent when the gold or silver rate
    # has actually changed since the last run — no change, no notification.
    price_changed = (gold_change != 0) or (silver_change != 0)

    if price_changed:
        users = load_users()
        for user in users:
            if not user["enable_telegram"]:
                log(f"Telegram disabled for {user['name']}; skipping.")
                continue

            user_recommendation = build_recommendation(gold, history_before, buy_target=user["buy_target"])
            message = format_message(gold, gold_change, silver_change, user_recommendation)
            send_message(message, chat_id=user["chat_id"])
    else:
        log("No change in gold/silver rate; skipping all Telegram alerts.")

    log("Application finished successfully")


if __name__ == "__main__":
    try:
        run()
    except Exception as exc:
        log(str(exc), "ERROR")
        sys.exit(1)
