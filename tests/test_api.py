"""
Basic tests that don't require live network/API/Sheets access.
Run with: pytest tests/
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from modules.analytics import moving_average, trend, volatility
from modules.recommendation import recommendation_label


def sample_history():
    return pd.DataFrame({
        "Gold 22K": [13000, 13100, 13050, 13000, 12950, 12900, 12850],
        "Silver": [200, 202, 201, 199, 198, 197, 196],
    })


def test_moving_average():
    df = sample_history()
    assert moving_average(df, "Gold 22K", 3) == round((12950 + 12900 + 12850) / 3, 2)


def test_trend_down():
    df = sample_history()
    assert trend(df) == "DOWN"


def test_volatility_not_none():
    df = sample_history()
    assert volatility(df, "Gold 22K") is not None


def test_recommendation_label_bounds():
    assert recommendation_label(95) == "🟢 Excellent Buy"
    assert recommendation_label(10) == "🔴 Don't Buy"
