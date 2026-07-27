"""
Shared utility helpers.
"""

from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))


def now_ist() -> datetime:
    """
    Return the current time as a timezone-aware datetime in IST
    (Asia/Kolkata, UTC+5:30).

    GitHub Actions runners default to UTC, so anywhere we write a
    timestamp (logs, Google Sheet rows, Telegram messages) should go
    through this instead of datetime.now().
    """
    return datetime.now(timezone.utc).astimezone(IST)
