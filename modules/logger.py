"""
Simple timestamped logger, matching the log() helper from the Colab notebook.
All timestamps are in IST, regardless of the server/runner's local timezone.
"""

from modules.utils import now_ist


def log(message, level="INFO"):
    """Print a timestamped log line, e.g. [INFO] 2026-07-27 12:00:00 IST - message"""
    now = now_ist().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{level}] {now} IST - {message}")


def safe_execute(function, *args, **kwargs):
    """Execute a function safely, logging any exception instead of crashing."""
    try:
        return function(*args, **kwargs)
    except Exception as ex:
        log(str(ex), "ERROR")
        return None
