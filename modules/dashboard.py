"""
Dashboard module — writes a live summary into the "Dashboard" worksheet
tab of the same Google Spreadsheet, so you get an always-up-to-date
snapshot without opening the raw Gold_Rates history tab.
"""

from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials

from config import CONFIG
from modules.sheets import get_worksheet
from modules.logger import log

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_dashboard_worksheet():
    """Return the Dashboard worksheet, creating it if it doesn't exist yet."""
    # Reuse the same authenticated client as sheets.py by opening the parent spreadsheet
    gold_ws = get_worksheet()
    spreadsheet = gold_ws.spreadsheet

    try:
        return spreadsheet.worksheet(CONFIG["DASHBOARD_NAME"])
    except gspread.WorksheetNotFound:
        return spreadsheet.add_worksheet(title=CONFIG["DASHBOARD_NAME"], rows=30, cols=4)


def update_dashboard(gold, analytics_summary, recommendation):
    """
    Overwrite the Dashboard tab with the latest snapshot:
    rates, moving averages, high/low, volatility, buy score, recommendation.
    """
    ws = get_dashboard_worksheet()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows = [
        ["Metric", "Value"],
        ["Last Updated", now],
        ["Gold 22K", gold["gold22"]],
        ["Gold 24K", gold["gold24"]],
        ["Silver", gold["silver"]],
        ["Platinum", gold["platinum"]],
        ["7-Day Average (22K)", analytics_summary.get("avg7")],
        ["30-Day Average (22K)", analytics_summary.get("avg30")],
        ["90-Day Average (22K)", analytics_summary.get("avg90")],
        ["Highest (22K)", analytics_summary.get("highest")],
        ["Lowest (22K)", analytics_summary.get("lowest")],
        ["Volatility (22K)", analytics_summary.get("volatility")],
        ["Trend", analytics_summary.get("trend")],
        ["Buy Score", recommendation.get("score")],
        ["Recommendation", recommendation.get("label")],
        ["Reasons", "; ".join(recommendation.get("reasons", []))],
    ]

    ws.clear()
    ws.update(range_name="A1", values=rows)
    log("Dashboard tab updated.")
