"""
========================================================
Gold Intelligence System
Configuration Module
========================================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Config:

    # -----------------------------
    # Google Sheets
    # -----------------------------
    SPREADSHEET_ID = "1OWl5vSFV3Gbr-M6qL5fTvO6igzmb484mYWUvDkzYm3U"

    GOLD_RATES_SHEET = "Gold_Rates"

    DASHBOARD_SHEET = "Dashboard"

    SETTINGS_SHEET = "Settings"

    LOGS_SHEET = "Logs"

    # -----------------------------
    # API
    # -----------------------------
    GRAPHQL_URL = (
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
    )

    USER_AGENT = "Gold Intelligence System"

    # -----------------------------
    # Analytics
    # -----------------------------
    SHORT_WINDOW = 7

    MEDIUM_WINDOW = 30

    LONG_WINDOW = 90

    BUY_TARGET = 13000

    # -----------------------------
    # Telegram
    # -----------------------------
    ENABLE_TELEGRAM = False

    BOT_TOKEN = ""

    CHAT_ID = ""
