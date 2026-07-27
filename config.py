# ============================================
# GOLD INTELLIGENCE CONFIGURATION
# ============================================

CONFIG = {

    # -----------------------------
    # Google Sheets
    # -----------------------------
    "SPREADSHEET_ID": "1OWl5vSFV3Gbr-M6qL5fTvO6igzmb484mYWUvDkzYm3U",

    "WORKSHEET_NAME": "Gold_Rates",

    "DASHBOARD_NAME": "Dashboard",

    # -----------------------------
    # GraphQL API
    # -----------------------------
    "GRAPHQL_URL":
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
    "&variables={}",

    # -----------------------------
    # User Settings
    # -----------------------------
    "BUY_TARGET": 13000,

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
    "SAVE_IF_NO_CHANGE": False,

    # -----------------------------
    # Telegram
    # -----------------------------
    "ENABLE_TELEGRAM": False,

    "BOT_TOKEN": "",

    "CHAT_ID": "",

}
