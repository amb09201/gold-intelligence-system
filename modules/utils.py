"""
General utility/helper functions used across the Gold Intelligence System.
"""

from datetime import datetime, timezone


def utc_now_iso() -> str:
    """Return the current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def safe_float(value, default=0.0) -> float:
    """Safely convert a value to float, returning default on failure."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def percent_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values."""
    old_value = safe_float(old_value)
    new_value = safe_float(new_value)
    if old_value == 0:
        return 0.0
    return ((new_value - old_value) / old_value) * 100


def chunk_list(items: list, chunk_size: int):
    """Yield successive chunks of a given size from a list."""
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]
