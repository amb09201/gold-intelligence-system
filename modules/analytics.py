"""
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
