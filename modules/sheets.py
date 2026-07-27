"""
Sheets module — Google Sheets read/write for the Gold_Rates worksheet.

Column layout (row order matters — must match the header row in the sheet):
Timestamp | Date | Time | Gold 14K | Gold 18K | Gold 22K | Gold 24K |
Silver | Platinum | Gold 22K Change | Silver Change | Buy Score |
Recommendation | Notes
"""

from datetime import datetime

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

from config import CONFIG
from modules.logger import log

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

_worksheet = None  # cached handle for this process


def get_worksheet():
    """Authenticate and return the Gold_Rates worksheet (cached per run)."""
    global _worksheet
    if _worksheet is not None:
        return _worksheet

    credentials = Credentials.from_service_account_file(
        CONFIG["GOOGLE_SERVICE_ACCOUNT_FILE"], scopes=SCOPES
    )
    gc = gspread.authorize(credentials)
    spreadsheet = gc.open_by_key(CONFIG["SPREADSHEET_ID"])
    _worksheet = spreadsheet.worksheet(CONFIG["WORKSHEET_NAME"])
    return _worksheet


def safe_int_conversion(value):
    """Safely convert a value to int, defaulting to 0 on failure."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


def get_previous_rates():
    """Return the most recently saved row (as a dict), or None if the sheet is empty."""
    worksheet = get_worksheet()
    records = worksheet.get_all_records()

    if len(records) == 0:
        return None

    return records[-1]


def should_save(gold):
    """
    Decide whether today's rates differ from the last saved row.
    Always saves if there is no previous row, or if SAVE_IF_NO_CHANGE is True.
    """
    if CONFIG.get("SAVE_IF_NO_CHANGE"):
        return True

    previous = get_previous_rates()
    if previous is None:
        return True

    return not (
        safe_int_conversion(previous.get("Gold 22K", 0)) == gold["gold22"]
        and safe_int_conversion(previous.get("Silver", 0)) == gold["silver"]
        and safe_int_conversion(previous.get("Platinum", 0)) == gold["platinum"]
    )


def calculate_changes(gold):
    """Return (gold_22k_change, silver_change) vs the previously saved row."""
    previous = get_previous_rates()

    if previous is None:
        return 0, 0

    previous_gold = safe_int_conversion(previous.get("Gold 22K", 0))
    previous_silver = safe_int_conversion(previous.get("Silver", 0))

    gold_change = gold["gold22"] - previous_gold
    silver_change = gold["silver"] - previous_silver

    return gold_change, silver_change


def save_to_google_sheet(gold, buy_score="", recommendation_text="", notes=""):
    """Append a new row of rates (+ optional score/recommendation) to the sheet."""
    worksheet = get_worksheet()

    gold_change, silver_change = calculate_changes(gold)
    now = datetime.now()

    worksheet.append_row([
        now.strftime("%Y-%m-%d %H:%M:%S"),
        now.strftime("%Y-%m-%d"),
        now.strftime("%H:%M:%S"),

        gold["gold14"],
        gold["gold18"],
        gold["gold22"],
        gold["gold24"],

        gold["silver"],
        gold["platinum"],

        gold_change,
        silver_change,

        buy_score,
        recommendation_text,
        notes,
    ])

    log("Rates saved to Google Sheet successfully.")


def read_history():
    """Read the full rate history from the sheet as a numeric-typed DataFrame."""
    worksheet = get_worksheet()
    records = worksheet.get_all_records()

    df = pd.DataFrame(records)
    if df.empty:
        return df

    numeric_columns = [
        "Gold 14K", "Gold 18K", "Gold 22K", "Gold 24K",
        "Silver", "Platinum", "Gold 22K Change", "Silver Change", "Buy Score",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df
