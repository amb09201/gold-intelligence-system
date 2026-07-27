"""
==========================================================
Gold Intelligence System
Google Sheets Module
==========================================================

Author : Mahesh Babu
Description:
Handles all Google Sheets operations.

Responsibilities
----------------
✔ Connect to Google Sheets
✔ Read historical data
✔ Read previous rates
✔ Save latest rates
✔ Update dashboard
✔ Write logs
✔ Load application settings
"""

from datetime import datetime

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

from config import Config
from modules.logger import logger


class GoogleSheets:
    """
    Google Sheets Manager
    """

    def __init__(self, credentials_file: str):

        self.credentials_file = credentials_file

        self.client = None
        self.workbook = None

        self.gold_sheet = None
        self.dashboard_sheet = None
        self.settings_sheet = None
        self.logs_sheet = None

    # ======================================================
    # Connection
    # ======================================================

    def connect(self):
        """
        Connect to Google Sheets.
        """

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

        self.settings_sheet = self.workbook.worksheet(
            Config.SETTINGS_SHEET
        )

        self.logs_sheet = self.workbook.worksheet(
            Config.LOGS_SHEET
        )

        logger.info("Connected to Google Sheets")

    # ======================================================
    # Read Historical Data
    # ======================================================

    def read_history(self):
        """
        Returns all historical data as a Pandas DataFrame.
        """

        records = self.gold_sheet.get_all_records()

        df = pd.DataFrame(records)

        if df.empty:
            return df

        numeric_columns = [

            "Gold 14K",
            "Gold 18K",
            "Gold 22K",
            "Gold 24K",
            "Silver",
            "Platinum",
            "Gold 22K Change",
            "Silver Change",
            "Buy Score"

        ]

        for column in numeric_columns:

            if column in df.columns:

                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

        return df

    # ======================================================
    # Previous Rates
    # ======================================================

    def get_previous_rates(self):
        """
        Returns the latest saved row.
        """

        records = self.gold_sheet.get_all_records()

        if len(records) == 0:
            return None

        return records[-1]

    # ======================================================
    # Save Today's Rates
    # ======================================================

    def save_rates(
        self,
        gold,
        gold_change,
        silver_change,
        buy_score,
        recommendation,
        notes=""
    ):
        """
        Save today's precious metal rates.
        """

        now = datetime.now()

        self.gold_sheet.append_row([

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
            recommendation,
            notes

        ])

        logger.info("Today's rates saved successfully.")

    # ======================================================
    # Dashboard
    # ======================================================

    def update_dashboard(self, dashboard):
        """
        Update Dashboard worksheet.
        """

        updates = {

            "B2": dashboard["latest_gold22"],
            "B3": dashboard["latest_gold24"],
            "B4": dashboard["latest_silver"],
            "B5": dashboard["latest_platinum"],

            "B7": dashboard["gold_change"],
            "B8": dashboard["silver_change"],

            "B10": dashboard["avg7"],
            "B11": dashboard["avg30"],
            "B12": dashboard["avg90"],

            "B14": dashboard["highest"],
            "B15": dashboard["lowest"],

            "B17": dashboard["buy_score"],
            "B18": dashboard["recommendation"],

            "B20": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        }

        for cell, value in updates.items():

            self.dashboard_sheet.update(
                cell,
                [[value]]
            )

        logger.info("Dashboard updated successfully.")

    # ======================================================
    # Logs
    # ======================================================

    def write_log(
        self,
        level,
        message
    ):
        """
        Write application logs to Google Sheets.
        """

        self.logs_sheet.append_row([

            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            level,

            message

        ])

    # ======================================================
    # Settings
    # ======================================================

    def load_settings(self):
        """
        Load application settings from Settings worksheet.
        """

        records = self.settings_sheet.get_all_records()

        settings = {}

        for row in records:

            settings[row["Parameter"]] = row["Value"]

        return settings

    # ======================================================
    # Duplicate Detection
    # ======================================================

    def has_price_changed(self, gold):
        """
        Returns True if Gold/Silver/Platinum prices changed.
        """

        previous = self.get_previous_rates()

        if previous is None:
            return True

        return not (

            int(previous["Gold 22K"]) == gold["gold22"] and

            int(previous["Silver"]) == gold["silver"] and

            int(previous["Platinum"]) == gold["platinum"]

        )
