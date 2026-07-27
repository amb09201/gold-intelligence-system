"""
Sheets module: reads/writes gold price data to Google Sheets.
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import config
from modules.logger import get_logger

logger = get_logger(__name__)

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]


def get_client():
    """Authenticate and return a gspread client."""
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        config.GOOGLE_SHEETS_CREDENTIALS_JSON, SCOPE
    )
    return gspread.authorize(creds)


def get_worksheet():
    """Open the configured spreadsheet/worksheet."""
    client = get_client()
    sheet = client.open_by_key(config.SPREADSHEET_ID)
    try:
        return sheet.worksheet(config.SHEET_NAME)
    except gspread.WorksheetNotFound:
        return sheet.add_worksheet(title=config.SHEET_NAME, rows=1000, cols=10)


def append_row(row: list):
    """Append a single row of data to the sheet."""
    try:
        ws = get_worksheet()
        ws.append_row(row)
        logger.info(f"Appended row to sheet: {row}")
    except Exception as exc:
        logger.error(f"Failed to append row to Google Sheets: {exc}")
        raise


def get_all_rows() -> list:
    """Retrieve all rows currently in the sheet."""
    ws = get_worksheet()
    return ws.get_all_records()
