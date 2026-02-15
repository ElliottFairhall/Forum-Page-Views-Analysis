"""Utility modules for the Intelligence Flux dashboard.

This package contains modules for:
- analytics: KPI calculations and anomaly detection
- data_loader: Data loading and validation
- plots: Themed Plotly visualizations
- text: Dashboard text content and guides
"""

from utils.analytics import detect_anomalies, get_audience_breakdown, get_kpis
from utils.data_loader import load_source_data
from utils.plots import (
    draw_anomaly_highlight,
    draw_bar_plot,
    draw_box_plot,
    draw_device_breakdown,
    draw_engagement_metrics,
    draw_geo_distribution,
    draw_line_plot,
    draw_regional_map,
)

__all__ = [
    "get_kpis",
    "detect_anomalies",
    "get_audience_breakdown",
    "load_source_data",
    "draw_line_plot",
    "draw_bar_plot",
    "draw_box_plot",
    "draw_geo_distribution",
    "draw_regional_map",
    "draw_device_breakdown",
    "draw_engagement_metrics",
    "draw_anomaly_highlight",
]
