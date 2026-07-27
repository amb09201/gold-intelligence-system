"""
<<<<<<< HEAD
Analytics module — moving averages, highs/lows, volatility, and trend
detection over the Gold_Rates history.
"""

from config import CONFIG


def moving_average(df, column, days):
    """Average of the last `days` non-null values in `column`."""
    if df.empty:
        return None

    values = df[column].dropna()
    if len(values) == 0:
        return None

    return round(values.tail(days).mean(), 2)


def highest_price(df, column):
    if df.empty:
        return None
    return df[column].max()


def lowest_price(df, column):
    if df.empty:
        return None
    return df[column].min()


def volatility(df, column):
    if df.empty:
        return None
    return round(df[column].std(), 2)


def trend(df, column="Gold 22K"):
    """Simple 3-point trend: UP / DOWN / SIDEWAYS / UNKNOWN (if <3 rows)."""
    if len(df) < 3:
        return "UNKNOWN"

    prices = df[column].tail(3).tolist()

    if prices[2] > prices[1] > prices[0]:
        return "UP"
    if prices[2] < prices[1] < prices[0]:
        return "DOWN"
    return "SIDEWAYS"


def build_analytics_summary(df):
    """Bundle all analytics into a single dict for reuse by recommendation/dashboard."""
    return {
        "avg7": moving_average(df, "Gold 22K", CONFIG["SHORT_MA"]),
        "avg30": moving_average(df, "Gold 22K", CONFIG["LONG_MA"]),
        "avg90": moving_average(df, "Gold 22K", CONFIG["VERY_LONG_MA"]),
        "silver_avg7": moving_average(df, "Silver", CONFIG["SHORT_MA"]),
        "highest": highest_price(df, "Gold 22K"),
        "lowest": lowest_price(df, "Gold 22K"),
        "volatility": volatility(df, "Gold 22K"),
        "trend": trend(df),
    }
=======
==========================================================
Gold Intelligence System
Analytics Module
==========================================================

Author : Mahesh Babu

Description
-----------
Provides all analytical calculations used by the application.

Responsibilities
----------------
✔ Moving averages
✔ Highest / Lowest price
✔ Daily changes
✔ Trend detection
✔ Consecutive rise/fall detection
✔ Volatility
✔ Dashboard metrics
"""

import pandas as pd

from config import Config
from modules.logger import logger


class Analytics:

    def __init__(self, history: pd.DataFrame):

        self.history = history.copy()

    # ======================================================
    # Utility
    # ======================================================

    def _series(self, column):

        if self.history.empty:
            return pd.Series(dtype=float)

        return self.history[column].dropna()

    # ======================================================
    # Moving Average
    # ======================================================

    def moving_average(self, column, window):

        values = self._series(column)

        if len(values) == 0:
            return None

        return round(values.tail(window).mean(), 2)

    # ======================================================
    # Highest
    # ======================================================

    def highest(self, column, window=None):

        values = self._series(column)

        if len(values) == 0:
            return None

        if window:
            values = values.tail(window)

        return float(values.max())

    # ======================================================
    # Lowest
    # ======================================================

    def lowest(self, column, window=None):

        values = self._series(column)

        if len(values) == 0:
            return None

        if window:
            values = values.tail(window)

        return float(values.min())

    # ======================================================
    # Volatility
    # ======================================================

    def volatility(self, column, window=30):

        values = self._series(column)

        if len(values) < 2:
            return None

        values = values.tail(window)

        return round(values.std(), 2)

    # ======================================================
    # Daily Change
    # ======================================================

    def latest_change(self, column):

        values = self._series(column)

        if len(values) < 2:
            return 0

        return float(values.iloc[-1] - values.iloc[-2])

    # ======================================================
    # Consecutive Down Days
    # ======================================================

    def consecutive_down(self, column):

        values = self._series(column)

        if len(values) < 2:
            return 0

        count = 0

        for i in range(len(values)-1, 0, -1):

            if values.iloc[i] < values.iloc[i-1]:
                count += 1
            else:
                break

        return count

    # ======================================================
    # Consecutive Up Days
    # ======================================================

    def consecutive_up(self, column):

        values = self._series(column)

        if len(values) < 2:
            return 0

        count = 0

        for i in range(len(values)-1, 0, -1):

            if values.iloc[i] > values.iloc[i-1]:
                count += 1
            else:
                break

        return count

    # ======================================================
    # Trend
    # ======================================================

    def trend(self, column):

        values = self._series(column)

        if len(values) < 3:
            return "UNKNOWN"

        last3 = values.tail(3).tolist()

        if last3[2] > last3[1] > last3[0]:
            return "UP"

        if last3[2] < last3[1] < last3[0]:
            return "DOWN"

        return "SIDEWAYS"

    # ======================================================
    # Percentage Change
    # ======================================================

    def percent_change(self, column):

        values = self._series(column)

        if len(values) < 2:
            return 0

        previous = values.iloc[-2]

        current = values.iloc[-1]

        if previous == 0:
            return 0

        pct = ((current - previous) / previous) * 100

        return round(pct, 2)

    # ======================================================
    # Distance From Target
    # ======================================================

    def distance_from_target(self, current_price):

        return current_price - Config.BUY_TARGET

    # ======================================================
    # Dashboard Metrics
    # ======================================================

    def dashboard_metrics(self):

        logger.info("Calculating dashboard metrics")

        latest_gold22 = self._series("Gold 22K").iloc[-1]
        latest_gold24 = self._series("Gold 24K").iloc[-1]
        latest_silver = self._series("Silver").iloc[-1]
        latest_platinum = self._series("Platinum").iloc[-1]

        return {

            "latest_gold22": latest_gold22,

            "latest_gold24": latest_gold24,

            "latest_silver": latest_silver,

            "latest_platinum": latest_platinum,

            "gold_change": self.latest_change("Gold 22K"),

            "silver_change": self.latest_change("Silver"),

            "avg7": self.moving_average(
                "Gold 22K",
                Config.SHORT_WINDOW
            ),

            "avg30": self.moving_average(
                "Gold 22K",
                Config.MEDIUM_WINDOW
            ),

            "avg90": self.moving_average(
                "Gold 22K",
                Config.LONG_WINDOW
            ),

            "highest": self.highest(
                "Gold 22K",
                Config.LONG_WINDOW
            ),

            "lowest": self.lowest(
                "Gold 22K",
                Config.LONG_WINDOW
            ),

            "volatility": self.volatility(
                "Gold 22K",
                Config.MEDIUM_WINDOW
            ),

            "trend": self.trend(
                "Gold 22K"
            ),

            "consecutive_down": self.consecutive_down(
                "Gold 22K"
            ),

            "consecutive_up": self.consecutive_up(
                "Gold 22K"
            ),

            "percent_change": self.percent_change(
                "Gold 22K"
            )

        }


        analytics.trend("Gold 22K")
        
        analytics.volatility("Gold 22K")
        
        analytics.highest("Gold 22K", 90)
        
        analytics.lowest("Gold 22K", 90)
        
        analytics.percent_change("Gold 22K")
        
        analytics.consecutive_down("Gold 22K")
>>>>>>> 80e5a703b5e9a10cbbb83800dbd2a9349bef8b52
