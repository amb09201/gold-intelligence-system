"""
Users module — reads the "Users" worksheet tab so the system can send a
personalized Buy Score/recommendation to multiple people, each with their
own Telegram chat and their own target buy price.

Expected "Users" tab layout:

    Name     | ChatID     | BuyTarget | EnableTelegram
    ---------|------------|-----------|----------------
    Mahesh   | 987654321  | 13000     | TRUE
    Friend1  | 123456789  | 12800     | TRUE
    Friend2  | 555555555  | 13500     | FALSE

If this tab doesn't exist, the system falls back to the single-user
CONFIG values (CHAT_ID / BUY_TARGET) exactly as before — nothing breaks
for a single-user setup.
"""

from config import CONFIG
from modules.sheets import get_worksheet
from modules.logger import log

USERS_SHEET_NAME = "Users"


def _parse_bool(value, default=True):
    if value is None or str(value).strip() == "":
        return default
    return str(value).strip().upper() in ("TRUE", "YES", "1")


def _parse_int(value, default=None):
    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        return default


def load_users():
    """
    Return a list of user dicts: [{"name": ..., "chat_id": ..., "buy_target": ..., "enable_telegram": ...}, ...]

    Falls back to a single "user" built from CONFIG (CHAT_ID/BUY_TARGET) if
    the "Users" tab doesn't exist — so existing single-user setups keep working.
    """
    try:
        gold_ws = get_worksheet()
        spreadsheet = gold_ws.spreadsheet
        users_ws = spreadsheet.worksheet(USERS_SHEET_NAME)
    except Exception as exc:
        log(f"No '{USERS_SHEET_NAME}' tab found, using single-user CONFIG instead: {exc}", "WARNING")
        return [{
            "name": "default",
            "chat_id": CONFIG.get("CHAT_ID", ""),
            "buy_target": CONFIG.get("BUY_TARGET", 13000),
            "enable_telegram": CONFIG.get("ENABLE_TELEGRAM", True),
        }]

    records = users_ws.get_all_records()  # [{"Name": ..., "ChatID": ..., "BuyTarget": ..., "EnableTelegram": ...}, ...]

    users = []
    for row in records:
        chat_id = str(row.get("ChatID", "")).strip()
        if not chat_id:
            continue  # skip rows without a chat ID — nowhere to send

        users.append({
            "name": row.get("Name", "").strip() or chat_id,
            "chat_id": chat_id,
            "buy_target": _parse_int(row.get("BuyTarget"), default=CONFIG.get("BUY_TARGET", 13000)),
            "enable_telegram": _parse_bool(row.get("EnableTelegram"), default=True),
        })

    if not users:
        log(f"'{USERS_SHEET_NAME}' tab has no valid rows; no alerts will be sent.", "WARNING")

    return users
