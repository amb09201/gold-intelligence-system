"""
Dashboard module: generates an HTML dashboard summarizing gold price data.
"""

import plotly.graph_objects as go
import plotly.io as pio

import config
from modules.logger import get_logger

logger = get_logger(__name__)


def build_dashboard(df, recommendation: dict, output_path: str = None) -> str:
    """
    Build an HTML dashboard with a price chart and the current recommendation.
    Returns the path to the generated HTML file.
    """
    output_path = output_path or config.DASHBOARD_OUTPUT_PATH

    fig = go.Figure()

    if not df.empty and "timestamp" in df.columns and "price" in df.columns:
        fig.add_trace(go.Scatter(x=df["timestamp"], y=df["price"], mode="lines", name="Gold Price"))

        if "ma_short" in df.columns:
            fig.add_trace(go.Scatter(x=df["timestamp"], y=df["ma_short"], mode="lines", name="Short MA"))
        if "ma_long" in df.columns:
            fig.add_trace(go.Scatter(x=df["timestamp"], y=df["ma_long"], mode="lines", name="Long MA"))

    fig.update_layout(
        title=f"Gold Price Dashboard — Recommendation: {recommendation.get('action', 'N/A')}",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_white",
    )

    pio.write_html(fig, file=output_path, auto_open=False)
    logger.info(f"Dashboard written to {output_path}")
    return output_path
