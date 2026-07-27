"""
Settings module — reads the "Settings" worksheet tab and merges those
values into CONFIG at runtime, so BUY_TARGET, ENABLE_TELEGRAM, and other
behavior can be changed directly from the spreadsheet without editing code
or GitHub secrets.

Expected "Settings" tab layout (two columns, header row + key/value rows):

    Parameter                  | Value
    ----------------------------|--------
    BUY_TARGET                  | 13000
    ENABLE_TELEGRAM             | FALSE
    TELEGRAM_CHAT_ID            |
    TELEGRAM_BOT_TOKEN          |
    DAILY_NOTIFICATION_TIME     | 9:00
    ALERT_ON_PRICE_CHANGE       | TRUE

TELEGRAM_CHAT_ID / TELEGRAM_BOT_TOKEN are optional in the sheet — if left
blank, the values already in CONFIG (from GitHub Secrets / .env) are kept.
Storing the bot token in the spreadsheet is not recommended since anyone
with access to the sheet could see and misuse it; leaving it blank and
using GitHub Secrets instead is safer.
"""

from config import CONFIG
from modules.sheets import get_worksheet
from modules.logger import log

SETTINGS_SHEET_NAME = "Settings"


def _parse_bool(value, default=False):
    if value is None or str(value).strip() == "":
        return default
    return str(value).strip().upper() in ("TRUE", "YES", "1")


def _parse_int(value, default=None):
    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        return default


def load_settings():
    """
    Read the Settings tab and return a dict of overrides.
    Returns {} (no overrides) if the tab is missing or unreadable —
    the app will simply keep using CONFIG defaults / secrets in that case.
    """
    try:
        gold_ws = get_worksheet()
        spreadsheet = gold_ws.spreadsheet
        settings_ws = spreadsheet.worksheet(SETTINGS_SHEET_NAME)
    except Exception as exc:
        log(f"Could not open '{SETTINGS_SHEET_NAME}' tab, using defaults: {exc}", "WARNING")
        return {}

    rows = settings_ws.get_all_records()  # [{"Parameter": "...", "Value": "..."}, ...]
    raw = {row.get("Parameter", "").strip(): row.get("Value", "") for row in rows if row.get("Parameter")}

    overrides = {}

    if "BUY_TARGET" in raw:
        parsed = _parse_int(raw["BUY_TARGET"])
        if parsed is not None:
            overrides["BUY_TARGET"] = parsed

    if "ENABLE_TELEGRAM" in raw:
        overrides["ENABLE_TELEGRAM"] = _parse_bool(raw["ENABLE_TELEGRAM"], default=CONFIG["ENABLE_TELEGRAM"])

    if "ALERT_ON_PRICE_CHANGE" in raw:
        overrides["ALERT_ON_PRICE_CHANGE"] = _parse_bool(raw["ALERT_ON_PRICE_CHANGE"], default=True)

    if "DAILY_NOTIFICATION_TIME" in raw and str(raw["DAILY_NOTIFICATION_TIME"]).strip():
        overrides["DAILY_NOTIFICATION_TIME"] = str(raw["DAILY_NOTIFICATION_TIME"]).strip()

    # Only override secrets if the sheet actually has a non-empty value.
    if str(raw.get("TELEGRAM_CHAT_ID", "")).strip():
        overrides["CHAT_ID"] = str(raw["TELEGRAM_CHAT_ID"]).strip()

    if str(raw.get("TELEGRAM_BOT_TOKEN", "")).strip():
        overrides["BOT_TOKEN"] = str(raw["TELEGRAM_BOT_TOKEN"]).strip()

    log(f"Loaded settings overrides from sheet: {list(overrides.keys())}")
    return overrides


def apply_settings():
    """Load settings from the sheet and merge them into CONFIG in place."""
    overrides = load_settings()
    CONFIG.update(overrides)
    return CONFIG
