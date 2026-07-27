"""
Basic tests for the api module.
Run with: pytest tests/
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
