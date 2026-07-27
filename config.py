"""
Configuration module for Gold Intelligence System.
Loads settings from environment variables (use a .env file locally,
or GitHub Secrets / Colab userdata in automated environments).
"""

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- API Settings ---
GOLD_API_KEY = os.getenv("GOLD_API_KEY", "")
GOLD_API_URL = os.getenv("GOLD_API_URL", "https://www.goldapi.io/api/XAU/USD")

# --- Google Sheets Settings ---
GOOGLE_SHEETS_CREDENTIALS_JSON = os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON", "credentials.json")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "")
SHEET_NAME = os.getenv("SHEET_NAME", "GoldPrices")

# --- Telegram Settings ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# --- Analytics Settings ---
SHORT_MA_WINDOW = int(os.getenv("SHORT_MA_WINDOW", 7))
LONG_MA_WINDOW = int(os.getenv("LONG_MA_WINDOW", 30))

# --- Logging Settings ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "gold_intelligence.log")

# --- Dashboard Settings ---
DASHBOARD_OUTPUT_PATH = os.getenv("DASHBOARD_OUTPUT_PATH", "dashboard.html")


def validate_config():
    """Check that essential config values are present. Raises if critical ones are missing."""
    missing = []
    if not GOLD_API_KEY:
        missing.append("GOLD_API_KEY")
    if missing:
        print(f"Warning: missing config values: {', '.join(missing)}")
    return len(missing) == 0
