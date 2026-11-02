"""Plotly figures for the page views explorer, in the Data Flakes style."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.analytics import month_heatmap, weekday_profile

PRIMARY = "#5E8FBA"
ACCENT = "#F67280"
PLUM = "#C06C84"
PEACH = "#F8B195"
SEQUENCE = [PRIMARY, PLUM, PEACH, "#6C5B7B", ACCENT, "#355C7D"]
DEVICE_COLOURS = {"Desktop": PRIMARY, "Mobile": PLUM, "Tablet": PEACH}
FONT = {"family": "Inter, sans-serif", "size": 13}
GRID = "rgba(128,128,128,0.18)"
MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
SMOOTH_DAYS = 7


def _style(fig: go.Figure, height: int = 360) -> go.Figure:
    """Apply the shared layout: transparent, light grid, Inter text."""
    fig.update_layout(
        height=height,
        margin={"t": 8, "b": 8, "l": 8, "r": 8},
        font=FONT,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_xaxes(gridcolor=GRID, zeroline=False)
    fig.update_yaxes(gridcolor=GRID, zeroline=False)
    return fig


def trend_figure(
    series: pd.DataFrame,
    smooth: bool,
    anomalies: pd.DataFrame | None,
    unit: str,
) -> go.Figure:
    """Line chart of page views over time.

    Args:
        series: Columns ``date`` and ``pageviews`` from ``resample_views``.
        smooth: Draw a 7-day average over the raw daily line (daily data only).
        anomalies: Flagged days to mark, or None.
        unit: ``"day"``, ``"week"`` or ``"month"``, used in the hover text.

    Returns:
        The figure.
    """
    fig = go.Figure()
    raw_colour = "rgba(94,143,186,0.35)" if smooth else PRIMARY
    fig.add_scatter(
        x=series["date"],
        y=series["pageviews"],
        name=f"Per {unit}",
        mode="lines",
        line={"color": raw_colour, "width": 1.5 if smooth else 2.5},
        hovertemplate="%{y:,.0f}",
    )
    if smooth:
        average = series["pageviews"].rolling(SMOOTH_DAYS, min_periods=1).mean()
        fig.add_scatter(
            x=series["date"],
            y=average,
            name=f"{SMOOTH_DAYS}-day average",
            mode="lines",
            line={"color": PRIMARY, "width": 2.5},
            hovertemplate="%{y:,.0f}",
        )
    if anomalies is not None and not anomalies.empty:
        fig.add_scatter(
            x=anomalies["date"],
            y=anomalies["pageviews"],
            name="Unusual day",
            mode="markers",
            marker={"color": ACCENT, "size": 9, "line": {"width": 1, "color": "white"}},
            hovertemplate="%{y:,.0f}",
        )
    _style(fig, 400)
    fig.update_layout(hovermode="x unified", legend={"orientation": "h", "y": 1.1})
    fig.update_yaxes(title="Page views")
    return fig


def top_countries_figure(df: pd.DataFrame, limit: int = 10) -> go.Figure:
    """Horizontal bars of the countries with the most page views.

    Args:
        df: Traffic data.
        limit: How many countries to show.

    Returns:
        The figure.
    """
    totals = df.groupby("country")["pageviews"].sum().nlargest(limit)
    share = totals / df["pageviews"].sum() * 100
    fig = go.Figure(
        go.Bar(
            x=totals.values,
            y=totals.index,
            orientation="h",
            marker_color=PRIMARY,
            text=[f"{s:.0f}%" for s in share],
            textposition="outside",
            cliponaxis=False,
            hovertemplate="%{x:,.0f} page views<extra></extra>",
        )
    )
    _style(fig, 60 + 32 * len(totals))
    fig.update_layout(margin={"t": 8, "b": 8, "l": 8, "r": 40})
    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(title="Page views")
    return fig


def share_figure(df: pd.DataFrame, column: str) -> go.Figure:
    """Horizontal bars of each segment's share of page views.

    Args:
        df: Traffic data.
        column: ``"device"`` or ``"region"``.

    Returns:
        The figure.
    """
    totals = df.groupby(column)["pageviews"].sum().sort_values(ascending=False)
    share = totals / totals.sum() * 100
    colours = [DEVICE_COLOURS.get(name, PRIMARY) for name in totals.index]
    fig = go.Figure(
        go.Bar(
            x=share.values,
            y=share.index,
            orientation="h",
            marker_color=colours,
            text=[f"{s:.0f}%" for s in share],
            textposition="outside",
            cliponaxis=False,
            hovertemplate="%{x:.1f}% of page views<extra></extra>",
        )
    )
    _style(fig, 60 + 40 * len(totals))
    fig.update_layout(margin={"t": 8, "b": 8, "l": 8, "r": 40})
    fig.update_xaxes(range=[0, max(share.max() * 1.2, 10)], ticksuffix="%")
    fig.update_yaxes(autorange="reversed")
    return fig


def map_figure(df: pd.DataFrame) -> go.Figure:
    """World map shaded by page views per country.

    Args:
        df: Traffic data with an ``iso_code`` column.

    Returns:
        The figure.
    """
    totals = df.groupby(["iso_code", "country"])["pageviews"].sum().reset_index()
    fig = go.Figure(
        go.Choropleth(
            locations=totals["iso_code"],
            z=totals["pageviews"],
            zmin=0,
            text=totals["country"],
            colorscale=[[0, "#DCE6F0"], [0.5, PRIMARY], [1, "#355C7D"]],
            marker_line_color="rgba(128,128,128,0.4)",
            marker_line_width=0.5,
            colorbar={"title": "Page views", "thickness": 12},
            hovertemplate="%{text}: %{z:,.0f}<extra></extra>",
        )
    )
    _style(fig, 420)
    fig.update_geos(
        showframe=False,
        showcoastlines=False,
        bgcolor="rgba(0,0,0,0)",
        projection_type="natural earth",
        landcolor="rgba(128,128,128,0.12)",
        showland=True,
    )
    return fig


def weekday_figure(df: pd.DataFrame) -> go.Figure:
    """Bars of average daily page views for each day of the week.

    Args:
        df: Traffic data.

    Returns:
        The figure.
    """
    profile = weekday_profile(df)
    fig = go.Figure(
        go.Bar(
            x=profile["weekday"],
            y=profile["pageviews"],
            marker_color=PRIMARY,
            hovertemplate="%{y:,.0f} a day<extra></extra>",
        )
    )
    _style(fig, 320)
    fig.update_yaxes(title="Average page views per day")
    return fig


def heatmap_figure(df: pd.DataFrame) -> go.Figure:
    """Heatmap of page views by year and calendar month.

    Args:
        df: Traffic data.

    Returns:
        The figure.
    """
    pivot = month_heatmap(df)
    fig = go.Figure(
        go.Heatmap(
            z=pivot.values,
            x=MONTHS,
            y=[str(year) for year in pivot.index],
            colorscale=[[0, "#EEF3F8"], [0.5, PRIMARY], [1, "#355C7D"]],
            colorbar={"title": "Page views", "thickness": 12},
            hovertemplate="%{y} %{x}: %{z:,.0f}<extra></extra>",
        )
    )
    _style(fig, 80 + 34 * len(pivot))
    fig.update_yaxes(autorange="reversed", showgrid=False)
    fig.update_xaxes(showgrid=False)
    return fig


def engagement_figure(df: pd.DataFrame) -> go.Figure:
    """Monthly session length and bounce rate, stacked.

    Args:
        df: Traffic data.

    Returns:
        The figure.
    """
    monthly = (
        df.set_index("date")
        .resample("MS")
        .agg({"session_duration": "mean", "bounce_rate": "mean"})
        .dropna()
    )
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)
    fig.add_scatter(
        x=monthly.index,
        y=monthly["session_duration"],
        name="Session length",
        mode="lines",
        line={"color": PRIMARY, "width": 2.5},
        hovertemplate="%{y:.0f} s",
        row=1,
        col=1,
    )
    fig.add_scatter(
        x=monthly.index,
        y=monthly["bounce_rate"] * 100,
        name="Bounce rate",
        mode="lines",
        line={"color": ACCENT, "width": 2.5},
        hovertemplate="%{y:.1f}%",
        row=2,
        col=1,
    )
    _style(fig, 440)
    fig.update_layout(hovermode="x unified", showlegend=False)
    fig.update_yaxes(title="Session length (s)", row=1, col=1)
    fig.update_yaxes(title="Bounce rate (%)", row=2, col=1)
    return fig
