"""
<<<<<<< HEAD
Basic tests that don't require live network/API/Sheets access.
=======
Basic tests for the api module.
>>>>>>> 80e5a703b5e9a10cbbb83800dbd2a9349bef8b52
Run with: pytest tests/
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

<<<<<<< HEAD
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
=======
from modules.utils import safe_float, percent_change, chunk_list


def test_safe_float_valid():
    assert safe_float("2385.12") == 2385.12


def test_safe_float_invalid():
    assert safe_float("not-a-number", default=0.0) == 0.0


def test_percent_change():
    assert percent_change(100, 110) == 10.0


def test_percent_change_zero_old_value():
    assert percent_change(0, 110) == 0.0


def test_chunk_list():
    chunks = list(chunk_list([1, 2, 3, 4, 5], 2))
    assert chunks == [[1, 2], [3, 4], [5]]
>>>>>>> 80e5a703b5e9a10cbbb83800dbd2a9349bef8b52
