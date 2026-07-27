"""
Recommendation module — turns live rates + analytics history into a
Buy Score (0-100) and a human-readable recommendation with reasons.

This is the same rule-based scoring logic validated in the Colab notebook,
formalized into a reusable module.
"""

from config import CONFIG
from modules.analytics import moving_average, trend


def calculate_buy_score(gold, history):
    """
    Returns (score: int, reasons: list[str]) based on current rates vs history.
    """
    score = 50
    reasons = []

    current = gold["gold22"]

    avg7 = moving_average(history, "Gold 22K", CONFIG["SHORT_MA"])
    avg30 = moving_average(history, "Gold 22K", CONFIG["LONG_MA"])

    if avg7 is not None and current < avg7:
        score += 10
        reasons.append("Below 7-day average")

    if avg30 is not None and current < avg30:
        score += 15
        reasons.append("Below 30-day average")

    if not history.empty and "Silver" in history.columns:
        silver_avg7 = history["Silver"].dropna().tail(CONFIG["SHORT_MA"]).mean()
        if silver_avg7 == silver_avg7 and gold["silver"] < silver_avg7:  # NaN-safe check
            score += 5
            reasons.append("Silver below 7-day average")

    t = trend(history)
    if t == "DOWN":
        score += 10
        reasons.append("Gold is in a short-term downtrend")

    if current <= CONFIG["BUY_TARGET"]:
        score += 20
        reasons.append("Below your target buying price")

    score = max(0, min(score, 100))
    return score, reasons


def recommendation_label(score):
    """Map a numeric score to an emoji-labeled recommendation string."""
    if score >= 90:
        return "🟢 Excellent Buy"
    if score >= 75:
        return "🟢 Strong Buy"
    if score >= 60:
        return "🟡 Buy"
    if score >= 40:
        return "⚪ Hold"
    if score >= 20:
        return "🟠 Wait"
    return "🔴 Don't Buy"


def build_recommendation(gold, history):
    """
    Convenience wrapper: returns a full recommendation dict ready to feed
    into Sheets, Telegram, and the dashboard.
    """
    score, reasons = calculate_buy_score(gold, history)
    label = recommendation_label(score)

    return {
        "score": score,
        "label": label,
        "reasons": reasons,
    }
