"""
Recommendation module: generates buy/sell/hold signals from analytics output.
"""

from modules.logger import get_logger

logger = get_logger(__name__)


def generate_recommendation(trend: str, volatility: float, volatility_threshold: float = 20.0) -> dict:
    """
    Generate a simple recommendation based on trend and volatility.

    Returns:
        {
            "action": "BUY" | "SELL" | "HOLD",
            "confidence": "HIGH" | "MEDIUM" | "LOW",
            "reason": str
        }
    """
    if trend == "up" and volatility < volatility_threshold:
        return {
            "action": "BUY",
            "confidence": "HIGH",
            "reason": "Upward trend with stable volatility.",
        }
    elif trend == "up":
        return {
            "action": "BUY",
            "confidence": "MEDIUM",
            "reason": "Upward trend but volatility is elevated.",
        }
    elif trend == "down" and volatility < volatility_threshold:
        return {
            "action": "SELL",
            "confidence": "HIGH",
            "reason": "Downward trend with stable volatility.",
        }
    elif trend == "down":
        return {
            "action": "SELL",
            "confidence": "MEDIUM",
            "reason": "Downward trend but volatility is elevated.",
        }
    else:
        return {
            "action": "HOLD",
            "confidence": "LOW",
            "reason": "No clear trend detected.",
        }
