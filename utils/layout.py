"""Page layout for the page views explorer."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.analytics import compact_number, percent_change
from utils.plots import (
    engagement_figure,
    heatmap_figure,
    map_figure,
    share_figure,
    top_countries_figure,
    trend_figure,
    weekday_figure,
)

SITE_URL = "https://www.data-flakes.dev"
ROOT = Path(__file__).resolve().parent.parent
GRANULARITY = {"Day": ("D", "day"), "Week": ("W", "week"), "Month": ("MS", "month")}


@dataclass(frozen=True)
class Filters:
    """The choices made in the sidebar.

    Attributes:
        start: First date, inclusive.
        end: Last date, inclusive.
        regions: Selected regions.
        countries: Selected countries.
        devices: Selected devices.
        freq: Pandas frequency code for the trend chart.
        unit: Plain-English unit for that frequency.
        smooth: Whether to overlay a 7-day average.
    """

    start: pd.Timestamp
    end: pd.Timestamp
    regions: list[str]
    countries: list[str]
    devices: list[str]
    freq: str
    unit: str
    smooth: bool


def _number(label: str) -> st.column_config.NumberColumn:
    """A number column with locale thousands separators."""
    return st.column_config.NumberColumn(label, format="localized")


def render_config() -> None:
    """Set the page configuration and load the stylesheet."""
    st.set_page_config(
        page_title="Page views explorer",
        page_icon=str(ROOT / "assets" / "images" / "favicon.png"),
        layout="wide",
    )
    css = (ROOT / "styles" / "main.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_topbar() -> None:
    """Show a plain breadcrumb back to the Data Flakes site."""
    st.markdown(
        f"""
        <nav class="site-bar">
            <a href="{SITE_URL}/" target="_blank">Data Flakes</a>
            <span>/</span>
            <a href="{SITE_URL}/projects/" target="_blank">Projects</a>
            <span>/</span>
            <span>Page views explorer</span>
        </nav>
        """,
        unsafe_allow_html=True,
    )


def render_intro(df: pd.DataFrame) -> None:
    """Introduce the page and say plainly that the data is synthetic.

    Args:
        df: The full traffic data.
    """
    st.title("Page views explorer")
    st.write(
        f"Daily page views for a web platform across {df['country'].nunique()} "
        f"countries, {df['date'].min():%B %Y} to {df['date'].max():%B %Y}. Filter by "
        "date, place and device, then look for patterns and unusual days."
    )
    st.caption(
        "The data is synthetic, generated for this demonstration. It describes no "
        "real site."
    )


def render_sidebar(df: pd.DataFrame) -> Filters:
    """Render the filters.

    Args:
        df: The full traffic data.

    Returns:
        The user's choices.
    """
    first, last = df["date"].min().date(), df["date"].max().date()
    with st.sidebar:
        st.header("Filters")
        picked = st.date_input(
            "Dates", (first, last), min_value=first, max_value=last, key="dates"
        )
        start, end = picked if len(picked) == 2 else (first, last)
        regions = st.multiselect(
            "Regions",
            sorted(df["region"].unique()),
            default=sorted(df["region"].unique()),
            key="regions",
        )
        country_options = sorted(df[df["region"].isin(regions)]["country"].unique())
        countries = st.multiselect(
            "Countries", country_options, default=country_options, key="countries"
        )
        devices = st.multiselect(
            "Devices",
            sorted(df["device"].unique()),
            default=sorted(df["device"].unique()),
            key="devices",
        )
        view = st.segmented_control("Trend by", list(GRANULARITY), default="Week")
        freq, unit = GRANULARITY[view or "Week"]
        smooth = st.toggle(
            "7-day average", value=True, disabled=freq != "D", key="smooth"
        )
    return Filters(
        pd.Timestamp(start),
        pd.Timestamp(end),
        regions,
        countries,
        devices,
        freq,
        unit,
        smooth and freq == "D",
    )


def render_metrics(current: dict, previous: dict | None) -> None:
    """Show the four headline numbers with change against the previous period.

    Args:
        current: KPIs for the selected period.
        previous: KPIs for the period of equal length just before, or None.
    """

    def delta(key: str) -> str | None:
        if not previous:
            return None
        change = percent_change(current[key], previous[key])
        return None if change is None else f"{change:+.1f}%"

    cols = st.columns(4)
    cols[0].metric(
        "Page views", compact_number(current["total_views"]), delta("total_views")
    )
    cols[1].metric(
        "Average per day", f"{current['avg_daily_views']:,}", delta("avg_daily_views")
    )
    cols[2].metric(
        "Session length", f"{current['avg_session']:.0f} s", delta("avg_session")
    )
    cols[3].metric(
        "Bounce rate",
        f"{current['avg_bounce'] * 100:.1f}%",
        delta("avg_bounce"),
        delta_color="inverse",
        help="Share of visits that left after one page. Lower is better.",
    )
    st.caption("Changes compare with the period of equal length just before.")


def render_trend(
    series: pd.DataFrame, filters: Filters, anomalies: pd.DataFrame | None
) -> None:
    """Draw the trend chart.

    Args:
        series: Page views per period.
        filters: The current filters.
        anomalies: Unusual days to mark when viewing by day.
    """
    st.subheader("Page views over time")
    st.plotly_chart(
        trend_figure(series, filters.smooth, anomalies, filters.unit), width="stretch"
    )


def render_breakdown(df: pd.DataFrame) -> None:
    """Show the deeper views, one per tab.

    Args:
        df: The filtered traffic data.
    """
    st.subheader("Breakdown")
    where, who, when, engagement = st.tabs(["Where", "Who", "When", "Engagement"])
    with where:
        st.caption("Page views by country. Percentages are each country's share.")
        st.plotly_chart(map_figure(df), width="stretch")
        st.plotly_chart(top_countries_figure(df), width="stretch")
    with who:
        left, right = st.columns(2)
        left.caption("Share of page views by device")
        left.plotly_chart(share_figure(df, "device"), width="stretch")
        right.caption("Share of page views by region")
        right.plotly_chart(share_figure(df, "region"), width="stretch")
    with when:
        left, right = st.columns([2, 3])
        left.caption("Average page views for each day of the week")
        left.plotly_chart(weekday_figure(df), width="stretch")
        right.caption("Total page views by year and month, to show seasonality")
        right.plotly_chart(heatmap_figure(df), width="stretch")
    with engagement:
        st.caption("How long visits last and how many leave after one page.")
        st.plotly_chart(engagement_figure(df), width="stretch")


def render_anomalies(anomalies: pd.DataFrame) -> None:
    """List the days that stood out from their surroundings.

    Args:
        anomalies: Output of ``analytics.rolling_anomalies``.
    """
    st.subheader("Unusual days")
    st.write(
        "A day is flagged when its page views are far from the median of the "
        "surrounding four weeks, measured with a robust score so a few spikes "
        "cannot hide others."
    )
    if anomalies.empty:
        st.info("No unusual days in this selection.")
        return
    table = anomalies.assign(
        change=(anomalies["pageviews"] / anomalies["expected"] - 1) * 100
    )[["date", "pageviews", "expected", "change", "score"]]
    st.dataframe(
        table.sort_values("score", key=abs, ascending=False).head(15),
        hide_index=True,
        width="stretch",
        column_config={
            "date": st.column_config.DateColumn("Date", format="D MMM YYYY"),
            "pageviews": st.column_config.NumberColumn(
                "Page views", format="localized"
            ),
            "expected": _number("Typical"),
            "change": st.column_config.NumberColumn("Vs typical", format="%+.0f%%"),
            "score": st.column_config.NumberColumn("Score", format="%+.1f"),
        },
    )


def render_footer() -> None:
    """Show a one-line footer linking back to the Data Flakes site."""
    st.markdown(
        f"""
        <footer class="site-foot">
            Synthetic data for demonstration. Built by Elliott Fairhall; more at
            <a href="{SITE_URL}/" target="_blank">data-flakes.dev</a>.
        </footer>
        """,
        unsafe_allow_html=True,
    )
