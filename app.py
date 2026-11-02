"""Page views explorer: entry point."""

from pathlib import Path

import pandas as pd
import streamlit as st

from utils import analytics
from utils.data_loader import load_source_data
from utils.layout import (
    render_anomalies,
    render_breakdown,
    render_config,
    render_footer,
    render_intro,
    render_metrics,
    render_sidebar,
    render_topbar,
    render_trend,
)

CSV_FILE = Path(__file__).parent / "assets" / "data" / "platform-traffic.csv"


@st.cache_data
def get_data() -> pd.DataFrame:
    """Load and validate the traffic data once per session."""
    return load_source_data(CSV_FILE)


def main() -> None:
    """Render the page. Everything updates as the filters change."""
    render_config()
    render_topbar()

    try:
        df = get_data()
    except FileNotFoundError:
        st.error(
            "Data file missing. Run `python scripts/synthesize_data.py` to create it."
        )
        return
    except ValueError as error:
        st.error(f"The data file is not valid: {error}")
        return

    render_intro(df)
    filters = render_sidebar(df)
    selected = analytics.filter_frame(
        df,
        filters.start,
        filters.end,
        filters.regions,
        filters.devices,
        filters.countries,
    )
    if selected.empty:
        st.warning("Nothing matches these filters. Widen the dates or segments.")
        render_footer()
        return

    before = analytics.filter_segments(
        analytics.previous_period(df, filters.start, filters.end),
        filters.regions,
        filters.devices,
        filters.countries,
    )
    render_metrics(
        analytics.get_kpis(selected),
        analytics.get_kpis(before) if len(before) else None,
    )

    anomalies = analytics.rolling_anomalies(selected)
    series = analytics.resample_views(selected, filters.freq)
    render_trend(series, filters, anomalies if filters.freq == "D" else None)
    render_breakdown(selected)
    render_anomalies(anomalies)
    render_footer()


if __name__ == "__main__":
    main()
