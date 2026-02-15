"""Visualization functions for the Intelligence Flux dashboard.

This module provides themed Plotly chart functions with a consistent
high-fidelity aesthetic (soft rose and sky color palette).
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# High-Fidelity Color Palette (V3)
COLORS: dict[str, str] = {
    "background": "#0f172a",
    "foreground": "#f8fafc",
    "primary": "#fda4af",  # Rose 300
    "secondary": "#7dd3fc",  # Sky 300
    "grid": "rgba(255, 255, 255, 0.05)",
    "muted": "rgba(148, 163, 184, 0.2)",
    "accent": "#f0abfc",  # Fuchsia 300
}


def _apply_theme(fig: go.Figure, title_size: int = 24) -> go.Figure:
    """Apply the soft high-fidelity theme to a Plotly figure.

    Configures consistent styling including dark background, custom fonts,
    hover labels, and axis formatting.

    Args:
        fig: Plotly Figure object to style.
        title_size: Font size for the chart title. Default is 24.

    Returns:
        The styled Figure object (modified in place).
    """
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=COLORS["foreground"],
        font_family="Inter",
        hoverlabel={
            "bgcolor": "#1e293b",
            "font_size": 14,
            "font_family": "Inter",
            "bordercolor": COLORS["secondary"],
        },
        margin={"l": 50, "r": 50, "t": 100, "b": 50},
        xaxis={
            "gridcolor": COLORS["grid"],
            "zerolinecolor": COLORS["grid"],
            "showgrid": False,
            "tickfont": {
                "family": "Inter",
                "size": 12,
                "color": "rgba(248,250,252,0.5)",
            },
        },
        yaxis={
            "gridcolor": COLORS["grid"],
            "zerolinecolor": COLORS["grid"],
            "showgrid": True,
            "tickprefix": " ",
            "tickfont": {
                "family": "Inter",
                "size": 12,
                "color": "rgba(248,250,252,0.5)",
            },
        },
        title={
            "font": {
                "size": title_size,
                "color": COLORS["foreground"],
                "family": "Outfit",
            },
            "x": 0.02,
            "y": 0.95,
        },
        legend={"font": {"family": "Inter", "size": 12}, "bgcolor": "rgba(0,0,0,0)"},
    )
    return fig


def draw_line_plot(df: pd.DataFrame) -> go.Figure:
    """Draw a premium line plot of Impression Flux (daily pageviews).

    Creates a time series visualization showing aggregate daily pageviews
    with a smooth rose-colored line.

    Args:
        df: DataFrame with 'date' and 'pageviews' columns.

    Returns:
        Themed Plotly Figure with the line chart.

    Example:
        >>> fig = draw_line_plot(traffic_df)
        >>> st.plotly_chart(fig, use_container_width=True)
    """
    daily_df = df.groupby("date")["pageviews"].sum().reset_index()
    fig = px.line(
        daily_df,
        x="date",
        y="pageviews",
        title="Impression Flux",
        labels={"date": "Timeline", "pageviews": "Aggregate Impressions"},
        color_discrete_sequence=[COLORS["primary"]],
    )
    fig.update_traces(line={"width": 2.5})
    return _apply_theme(fig)


def draw_bar_plot(df: pd.DataFrame) -> go.Figure:
    """Draw a premium bar plot of Cyclical Variance (seasonality).

    Creates a grouped bar chart showing average monthly pageviews by year
    to reveal seasonal patterns.

    Args:
        df: DataFrame with 'date' and 'pageviews' columns.

    Returns:
        Themed Plotly Figure with the grouped bar chart.

    Example:
        >>> fig = draw_bar_plot(traffic_df)
        >>> st.plotly_chart(fig, use_container_width=True)
    """
    df_bar = df.copy()
    df_bar["year"] = df_bar["date"].dt.year
    df_bar["month"] = df_bar["date"].dt.month_name()
    monthly_avg = df_bar.groupby(["year", "month"])["pageviews"].mean().reset_index()
    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    fig = px.bar(
        monthly_avg,
        x="month",
        y="pageviews",
        color="year",
        barmode="group",
        category_orders={"month": month_order},
        title="Cyclical Variance (Seasonal Distribution)",
        labels={
            "pageviews": "Avg Daily Impressions",
            "month": "Period",
            "year": "Year",
        },
        color_discrete_sequence=[
            COLORS["primary"],
            COLORS["secondary"],
            COLORS["accent"],
        ],
    )
    return _apply_theme(fig)


def draw_box_plot(df: pd.DataFrame) -> tuple[go.Figure, go.Figure]:
    """Draw premium Evolutionary Variance box plots (annual and monthly).

    Creates two box plots showing pageview distribution by year and by month
    to visualize statistical spread over time.

    Args:
        df: DataFrame with 'date' and 'pageviews' columns.

    Returns:
        Tuple of two themed Plotly Figures:
            - Annual box plot (by year)
            - Monthly box plot (by month abbreviation)

    Example:
        >>> fig_year, fig_month = draw_box_plot(traffic_df)
        >>> st.plotly_chart(fig_year)
        >>> st.plotly_chart(fig_month)
    """
    df_box = df.copy()
    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")
    month_order = [
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

    fig1 = px.box(
        df_box,
        x="year",
        y="pageviews",
        title="Evolutionary Variance (Annual)",
        color_discrete_sequence=[COLORS["primary"]],
    )
    fig2 = px.box(
        df_box,
        x="month",
        y="pageviews",
        category_orders={"month": month_order},
        title="Evolutionary Variance (Monthly)",
        color_discrete_sequence=[COLORS["secondary"]],
    )
    return _apply_theme(fig1), _apply_theme(fig2)


def draw_geo_distribution(df: pd.DataFrame) -> go.Figure:
    """Draw Source Concentration horizontal bar plot (top countries).

    Creates a horizontal bar chart showing the top 10 countries by
    total pageviews.

    Args:
        df: DataFrame with 'country' and 'pageviews' columns.

    Returns:
        Themed Plotly Figure with the horizontal bar chart.

    Example:
        >>> fig = draw_geo_distribution(traffic_df)
        >>> st.plotly_chart(fig, use_container_width=True)
    """
    geo_df = (
        df.groupby("country")["pageviews"]
        .sum()
        .reset_index()
        .sort_values("pageviews", ascending=True)
        .tail(10)
    )
    fig = px.bar(
        geo_df,
        x="pageviews",
        y="country",
        orientation="h",
        title="Source Concentration (Primary Locale)",
        labels={"pageviews": "Total Volume", "country": "Locale"},
        color_discrete_sequence=[COLORS["secondary"]],
    )
    return _apply_theme(fig)


def draw_regional_map(df: pd.DataFrame) -> go.Figure:
    """Draw an interactive Global Reach choropleth map.

    Creates a world map colored by pageview volume per country,
    using natural earth projection.

    Args:
        df: DataFrame with 'country', 'iso_code', and 'pageviews' columns.

    Returns:
        Themed Plotly Figure with the choropleth map.

    Example:
        >>> fig = draw_regional_map(traffic_df)
        >>> st.plotly_chart(fig, use_container_width=True)
    """
    geo_df = df.groupby(["country", "iso_code"])["pageviews"].sum().reset_index()
    fig = px.choropleth(
        geo_df,
        locations="iso_code",
        locationmode="ISO-3",
        color="pageviews",
        hover_name="country",
        title="Global Reach Index",
        color_continuous_scale=[
            [0, "#1e293b"],
            [0.5, COLORS["secondary"]],
            [1, COLORS["primary"]],
        ],
        height=700,
    )
    fig.update_geos(
        showcountries=True,
        countrycolor="rgba(255,255,255,0.1)",
        showcoastlines=True,
        coastlinecolor="rgba(255,255,255,0.1)",
        showland=True,
        landcolor="#1e293b",
        showocean=True,
        oceancolor="#0f172a",
        bgcolor="rgba(0,0,0,0)",
        projection_type="natural earth",
    )
    fig.update_layout(
        coloraxis_colorbar={"title": "Volume", "thickness": 15, "len": 0.5}
    )
    return _apply_theme(fig)


def draw_device_breakdown(df: pd.DataFrame) -> go.Figure:
    """Draw Interface Matrix donut chart (device distribution).

    Creates a donut chart showing pageview distribution by device type
    (Desktop, Mobile, Tablet).

    Args:
        df: DataFrame with 'device' and 'pageviews' columns.

    Returns:
        Themed Plotly Figure with the donut chart.

    Example:
        >>> fig = draw_device_breakdown(traffic_df)
        >>> st.plotly_chart(fig, use_container_width=True)
    """
    dev_df = df.groupby("device")["pageviews"].sum().reset_index()
    fig = px.pie(
        dev_df,
        values="pageviews",
        names="device",
        hole=0.7,
        title="Interface Matrix",
        color_discrete_sequence=[
            COLORS["primary"],
            COLORS["secondary"],
            COLORS["accent"],
        ],
    )
    fig.update_traces(marker={"line": {"color": COLORS["background"], "width": 2}})
    return _apply_theme(fig)


def draw_engagement_metrics(df: pd.DataFrame) -> go.Figure:
    """Draw User Flux Dynamics dual-axis chart with moving averages.

    Creates a time series with session duration and bounce rate,
    showing both raw daily values (faded) and 7-day moving averages.

    Args:
        df: DataFrame with 'date', 'session_duration', and 'bounce_rate' columns.

    Returns:
        Themed Plotly Figure with dual y-axes.

    Example:
        >>> fig = draw_engagement_metrics(traffic_df)
        >>> st.plotly_chart(fig, use_container_width=True)
    """
    eng_df = (
        df.groupby("date")
        .agg({"session_duration": "mean", "bounce_rate": "mean"})
        .reset_index()
    )
    # Apply 7-day moving average to reduce noise
    eng_df["duration_ma"] = eng_df["session_duration"].rolling(window=7).mean()
    eng_df["bounce_ma"] = eng_df["bounce_rate"].rolling(window=7).mean()

    fig = go.Figure()

    # Raw daily data (faded)
    fig.add_trace(
        go.Scatter(
            x=eng_df["date"],
            y=eng_df["session_duration"],
            name="Duration (Daily)",
            line={"color": COLORS["primary"], "width": 1},
            opacity=0.3,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=eng_df["date"],
            y=eng_df["bounce_rate"],
            name="Bounce Index (Daily)",
            yaxis="y2",
            line={"color": COLORS["secondary"], "width": 1},
            opacity=0.3,
        )
    )

    # Moving averages (stronger lines)
    fig.add_trace(
        go.Scatter(
            x=eng_df["date"],
            y=eng_df["duration_ma"],
            name="Duration (7d Trend)",
            line={"color": COLORS["primary"], "width": 3},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=eng_df["date"],
            y=eng_df["bounce_ma"],
            name="Bounce Index (7d Trend)",
            yaxis="y2",
            line={"color": COLORS["secondary"], "width": 3},
        )
    )

    fig.update_layout(
        title="User Flux Dynamics (Smooth Correlation)",
        yaxis={"title": "Stay Duration (s)", "range": [0, 200]},
        yaxis2={
            "title": "Bounce Index (%)",
            "overlaying": "y",
            "side": "right",
            "range": [0, 1],
            "showgrid": False,
        },
    )
    return _apply_theme(fig)


def draw_anomaly_highlight(df: pd.DataFrame, anomalies: pd.DataFrame) -> go.Figure:
    """Draw Signal Intelligence plot highlighting anomalous days.

    Creates a line chart with star markers on days identified as
    statistical outliers.

    Args:
        df: DataFrame with 'date' and 'pageviews' columns.
        anomalies: DataFrame of anomalous days (from detect_anomalies).

    Returns:
        Themed Plotly Figure with anomaly markers.

    Example:
        >>> anomalies = detect_anomalies(traffic_df)
        >>> fig = draw_anomaly_highlight(traffic_df, anomalies)
        >>> st.plotly_chart(fig, use_container_width=True)
    """
    daily_df = df.groupby("date")["pageviews"].sum().reset_index()
    fig = px.line(
        daily_df,
        x="date",
        y="pageviews",
        title="Signal Intelligence (Critical Outliers)",
        color_discrete_sequence=[COLORS["muted"]],
    )
    fig.add_trace(
        go.Scatter(
            x=anomalies["date"],
            y=anomalies["pageviews"],
            mode="markers",
            name="Critical Outlier",
            marker={
                "color": COLORS["primary"],
                "size": 12,
                "symbol": "star",
                "line": {"width": 1, "color": "white"},
            },
        )
    )
    return _apply_theme(fig)
