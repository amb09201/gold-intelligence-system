"""
Analytics module: computes trends and statistics from gold price history.
"""

import pandas as pd

import config
from modules.logger import get_logger

logger = get_logger(__name__)


def to_dataframe(rows: list) -> pd.DataFrame:
    """Convert a list of price records into a pandas DataFrame."""
    df = pd.DataFrame(rows)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")
    return df


def moving_averages(df: pd.DataFrame, price_col: str = "price") -> pd.DataFrame:
    """Add short and long moving average columns to the DataFrame."""
    df = df.copy()
    df["ma_short"] = df[price_col].rolling(window=config.SHORT_MA_WINDOW, min_periods=1).mean()
    df["ma_long"] = df[price_col].rolling(window=config.LONG_MA_WINDOW, min_periods=1).mean()
    return df


def compute_volatility(df: pd.DataFrame, price_col: str = "price") -> float:
    """Compute the standard deviation of prices as a simple volatility measure."""
    if df.empty:
        return 0.0
    return float(df[price_col].std())


def compute_trend(df: pd.DataFrame, price_col: str = "price") -> str:
    """
    Determine the overall trend ('up', 'down', 'flat') based on
    the short vs long moving averages.
    """
    if df.empty or len(df) < 2:
        return "flat"

    df = moving_averages(df, price_col)
    latest = df.iloc[-1]

    if latest["ma_short"] > latest["ma_long"]:
        return "up"
    elif latest["ma_short"] < latest["ma_long"]:
        return "down"
    return "flat"
