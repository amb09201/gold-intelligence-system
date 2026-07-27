"""
==========================================================
Google Sheets Module
==========================================================
"""

from datetime import datetime

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

from config import Config
from modules.logger import logger


class GoogleSheets:

    def __init__(self, credentials_file: str):

        self.credentials_file = credentials_file

        self.client = None

        self.workbook = None

        self.gold_sheet = None

        self.dashboard_sheet = None

        self.logs_sheet = None

        self.settings_sheet = None

    # -------------------------------------------------
    # Connect
    # -------------------------------------------------

    def connect(self):

        scopes = [

            "https://www.googleapis.com/auth/spreadsheets",

            "https://www.googleapis.com/auth/drive"

        ]

        credentials = Credentials.from_service_account_file(
            self.credentials_file,
            scopes=scopes
        )

        self.client = gspread.authorize(credentials)

        self.workbook = self.client.open_by_key(
            Config.SPREADSHEET_ID
        )

        self.gold_sheet = self.workbook.worksheet(
            Config.GOLD_RATES_SHEET
        )

        self.dashboard_sheet = self.workbook.worksheet(
            Config.DASHBOARD_SHEET
        )

        self.logs_sheet = self.workbook.worksheet(
            Config.LOGS_SHEET
        )

        self.settings_sheet = self.workbook.worksheet(
            Config.SETTINGS_SHEET
        )

        logger.info("Connected to Google Sheets")
