"""
Gold Intelligence System — Configuration

Values that are secret (spreadsheet ID, bot token, chat ID, service account
credentials) are read from environment variables so the same code works
locally (.env file) and in GitHub Actions (repo Secrets).
"""

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

CONFIG = {

    # -----------------------------
    # Google Sheets
    # -----------------------------
    "SPREADSHEET_ID": os.getenv("SPREADSHEET_ID", "1OWl5vSFV3Gbr-M6qL5fTvO6igzmb484mYWUvDkzYm3U"),
    "WORKSHEET_NAME": os.getenv("WORKSHEET_NAME", "Gold_Rates"),
    "DASHBOARD_NAME": os.getenv("DASHBOARD_NAME", "Dashboard"),

    # Path to the service account JSON key file.
    # Locally: point this at your downloaded credentials file.
    # In GitHub Actions: the workflow writes the GOOGLE_CREDENTIALS secret
    # out to this path before running main.py.
    "GOOGLE_SERVICE_ACCOUNT_FILE": os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json"),

    # -----------------------------
    # GraphQL API (Joyalukkas)
    # -----------------------------
    "GRAPHQL_URL": (
        "https://www.joyalukkas.in/graphql"
        "?query=query+getgoldrates{"
        "getgoldrates{"
        "Id Message Status metal_rate_time "
        "Data{"
        "Id BRANCH_CODE BRANCH_NAME "
        "GOLD_14KT_RATE GOLD_18KT_RATE "
        "GOLD_22KT_RATE GOLD_24KT_RATE "
        "SILVER_RATE SILVER_RATE100 "
        "SILVER_RATE999 PLATINUM_RATE "
        "__typename}"
        "__typename}}"
        "&operationName=getgoldrates"
        "&variables={}"
    ),

    # -----------------------------
    # User Settings
    # -----------------------------
    "BUY_TARGET": int(os.getenv("BUY_TARGET", 13000)),
    "CURRENCY": "₹",

    # -----------------------------
    # Analytics
    # -----------------------------
    "SHORT_MA": 7,
    "LONG_MA": 30,
    "VERY_LONG_MA": 90,

    # -----------------------------
    # Duplicate Detection
    # -----------------------------
    "SAVE_IF_NO_CHANGE": os.getenv("SAVE_IF_NO_CHANGE", "False") == "True",

    # -----------------------------
    # Alerting (overridable from the "Settings" sheet tab)
    # -----------------------------
    "ALERT_ON_PRICE_CHANGE": True,
    "DAILY_NOTIFICATION_TIME": "9:00",

    # -----------------------------
    # Telegram
    # -----------------------------
    "ENABLE_TELEGRAM": os.getenv("ENABLE_TELEGRAM", "True") == "True",
    "BOT_TOKEN": os.getenv("BOT_TOKEN", ""),
    "CHAT_ID": os.getenv("CHAT_ID", ""),
}
