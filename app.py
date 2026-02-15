"""Intelligence Flux Dashboard - Interactive Traffic Analytics.

A premium Streamlit dashboard for web platform traffic analysis,
featuring interactive visualizations, anomaly detection, and
geospatial analytics.
"""

import logging
from pathlib import Path

import streamlit as st

from utils import analytics, text
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Intelligence Flux",
    page_icon=":snowflake:",
    layout="wide",
)

# Project paths
CURRENT_DIR = Path(__file__).parent
CSV_FILE = CURRENT_DIR / "assets" / "data" / "platform-traffic.csv"
CSS_FILE = CURRENT_DIR / "styles" / "main.css"


def load_css(file_path: Path) -> None:
    """Inject custom CSS into the Streamlit app.

    Args:
        file_path: Path to the CSS file to load.
    """
    if file_path.exists():
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_header() -> None:
    """Render the premium header section with title and subtitle."""
    st.markdown(
        """
        <div class='header-container'>
            <h1 class='main-title'>Intelligence Flux</h1>
            <p class='sub-title'>TRANSFORMING COMPLEXITY INTO CLARITY</p>
        </div>
    """,
        unsafe_allow_html=True,
    )


def render_sidebar(df: "pd.DataFrame") -> tuple[list[str], list[str]]:
    """Render the sidebar with filter controls.

    Args:
        df: DataFrame with 'region' and 'device' columns for filter options.

    Returns:
        Tuple of (selected_regions, selected_devices) lists.
    """
    with st.sidebar:
        st.markdown(
            "<h2 style='font-family:Outfit; margin-bottom:0;'>Data Engine</h2>",
            unsafe_allow_html=True,
        )
        st.caption("Configuring high-fidelity signals.")
        st.markdown("---")

        selected_regions = st.multiselect(
            "Geography",
            options=sorted(df["region"].unique()),
            default=list(df["region"].unique()),
        )
        selected_devices = st.multiselect(
            "Platform segment",
            options=sorted(df["device"].unique()),
            default=list(df["device"].unique()),
        )

        st.markdown("---")
        st.caption("Environment: Intelligence Flux V3.0")
        st.caption("Aesthetic: Soft Rose / Sky")

        with st.expander("Quick Start Guide"):
            text.header_guide()

    return selected_regions, selected_devices


def render_metrics(kpis: dict[str, int | float]) -> None:
    """Render the KPI metrics row.

    Args:
        kpis: Dictionary with total_views, avg_daily_views, avg_session, avg_bounce.
    """
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Impressions", f"{kpis['total_views']:,}")
    c2.metric("Mean Daily Reach", f"{kpis['avg_daily_views']:,}")
    c3.metric("Retention/Stay", f"{kpis['avg_session']}s")
    c4.metric("Bounce Index", f"{kpis['avg_bounce'] * 100:.1f}%")


def main() -> None:
    """Execute the primary dashboard orchestration."""
    # Load CSS
    load_css(CSS_FILE)

    # Render header
    render_header()

    # Load data
    try:
        df = load_source_data(CSV_FILE)
    except FileNotFoundError:
        st.error("Data load failed. Please run: `python scripts/synthesize_data.py`")
        return
    except ValueError as e:
        st.error(f"Data validation failed: {e}")
        return

    # Sidebar filters
    selected_regions, selected_devices = render_sidebar(df)

    # Apply filters
    filtered_df = df[
        (df["region"].isin(selected_regions)) & (df["device"].isin(selected_devices))
    ]

    if filtered_df.empty:
        st.warning("Digital silence. Please adjust your filters.")
        return

    # Metrics row
    kpis = analytics.get_kpis(filtered_df)
    render_metrics(kpis)

    st.markdown("<br>", unsafe_allow_html=True)

    # Navigation tabs
    t1, t2, t3, t4, t5 = st.tabs(
        [
            "Project Overview",
            "Performance",
            "Global Reach",
            "Engagement",
            "Intelligence",
        ]
    )

    with t1:
        text.project_overview()

    with t2:
        st.plotly_chart(draw_line_plot(filtered_df), width="stretch")
        st.plotly_chart(draw_bar_plot(filtered_df), width="stretch")

    with t3:
        text.audience_info()
        st.plotly_chart(draw_regional_map(filtered_df), width="stretch")
        c_left, c_right = st.columns(2)
        c_left.plotly_chart(draw_geo_distribution(filtered_df), width="stretch")
        c_right.plotly_chart(draw_device_breakdown(filtered_df), width="stretch")

    with t4:
        text.performance_info()
        st.plotly_chart(draw_engagement_metrics(filtered_df), width="stretch")

    with t5:
        text.anomaly_info()
        anomalies = analytics.detect_anomalies(filtered_df)
        st.plotly_chart(draw_anomaly_highlight(filtered_df, anomalies), width="stretch")
        b1, b2 = draw_box_plot(filtered_df)
        st.plotly_chart(b1, width="stretch")
        st.plotly_chart(b2, width="stretch")


if __name__ == "__main__":
    main()
