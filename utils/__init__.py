"""Helper modules for the page views explorer.

- analytics: filtering, KPIs, comparison periods and anomaly detection
- data_loader: loading and validating the CSV
- plots: Plotly figures in the Data Flakes style
- layout: Streamlit page sections
- text: long-form guide text from the earlier version of the app
"""

from utils.analytics import (
    detect_anomalies,
    get_audience_breakdown,
    get_kpis,
    rolling_anomalies,
)
from utils.data_loader import load_source_data

__all__ = [
    "detect_anomalies",
    "get_audience_breakdown",
    "get_kpis",
    "load_source_data",
    "rolling_anomalies",
]
