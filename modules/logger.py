"""
Simple timestamped logger, matching the log() helper from the Colab notebook.
"""

from datetime import datetime


def log(message, level="INFO"):
    """Print a timestamped log line, e.g. [INFO] 2026-07-27 12:00:00 - message"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{level}] {now} - {message}")


def safe_execute(function, *args, **kwargs):
    """Execute a function safely, logging any exception instead of crashing."""
    try:
        return function(*args, **kwargs)
    except Exception as ex:
        log(str(ex), "ERROR")
        return None
