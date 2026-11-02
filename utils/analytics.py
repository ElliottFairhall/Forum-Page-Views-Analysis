"""Analytics functions for the Intelligence Flux dashboard.

This module provides KPI calculations, anomaly detection, and data
aggregation functions for web traffic analysis.
"""

import numpy as np
import pandas as pd
from scipy import stats


def get_kpis(df: pd.DataFrame) -> dict[str, int | float]:
    """Calculate high-level KPIs from traffic data.

    Computes aggregate metrics including total views, average daily views,
    mean session duration, and average bounce rate.

    Args:
        df: DataFrame containing traffic data with columns:
            - pageviews: Number of page views per record
            - date: Date of the traffic record
            - session_duration: Average session length in seconds
            - bounce_rate: Proportion of single-page sessions (0-1)

    Returns:
        Dictionary with keys:
            - total_views: Sum of all pageviews
            - avg_daily_views: Mean pageviews per day (integer)
            - avg_session: Mean session duration rounded to 2 decimals
            - avg_bounce: Mean bounce rate rounded to 4 decimals

    Example:
        >>> kpis = get_kpis(traffic_df)
        >>> print(f"Total views: {kpis['total_views']:,}")
    """
    total_views = int(df["pageviews"].sum())
    avg_daily_views = int(df.groupby("date")["pageviews"].sum().mean())
    avg_session = round(df["session_duration"].mean(), 2)
    avg_bounce = round(df["bounce_rate"].mean(), 4)

    return {
        "total_views": total_views,
        "avg_daily_views": avg_daily_views,
        "avg_session": avg_session,
        "avg_bounce": avg_bounce,
    }


def detect_anomalies(
    df: pd.DataFrame,
    threshold: float = 3.0,
) -> pd.DataFrame:
    """Detect anomalies in daily pageviews using Z-score method.

    Identifies days where pageview counts deviate significantly from the
    mean, using statistical Z-scores to flag outliers.

    Args:
        df: DataFrame containing traffic data with 'date' and 'pageviews' columns.
        threshold: Z-score threshold for anomaly detection. Default is 3.0,
            which flags values more than 3 standard deviations from the mean.

    Returns:
        DataFrame containing only anomalous days with columns:
            - date: Date of the anomaly
            - pageviews: Total pageviews on that day
            - is_anomaly: Boolean flag (always True in output)

    Example:
        >>> anomalies = detect_anomalies(traffic_df, threshold=2.5)
        >>> print(f"Found {len(anomalies)} anomalous days")
    """
    daily_df = df.groupby("date")["pageviews"].sum().reset_index()
    z_scores = np.abs(stats.zscore(daily_df["pageviews"]))
    daily_df["is_anomaly"] = z_scores > threshold
    return daily_df[daily_df["is_anomaly"]].copy()


def get_audience_breakdown(
    df: pd.DataFrame,
    dimension: str = "device",
) -> pd.DataFrame:
    """Aggregate pageviews by a specific dimension.

    Groups traffic data by a categorical dimension and sums pageviews
    for audience segmentation analysis.

    Args:
        df: DataFrame containing traffic data with 'pageviews' column
            and the specified dimension column.
        dimension: Column name to group by. Common values include
            'device', 'region', 'country'. Default is 'device'.

    Returns:
        DataFrame with the dimension column and aggregated 'pageviews'.

    Raises:
        KeyError: If the specified dimension column doesn't exist in df.

    Example:
        >>> device_breakdown = get_audience_breakdown(df, dimension='device')
        >>> regional_breakdown = get_audience_breakdown(df, dimension='region')
    """
    if dimension not in df.columns:
        raise KeyError(f"Dimension '{dimension}' not found in DataFrame columns")
    return df.groupby(dimension)["pageviews"].sum().reset_index()


def get_engagement_by_date(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate daily engagement metrics.

    Aggregates session duration, bounce rate, and pageviews by date
    to show engagement trends over time.

    Args:
        df: DataFrame containing traffic data with columns:
            - date: Date of the traffic record
            - session_duration: Session length in seconds
            - bounce_rate: Proportion of single-page sessions
            - pageviews: Number of page views

    Returns:
        DataFrame indexed by date with columns:
            - session_duration: Mean session duration for the day
            - bounce_rate: Mean bounce rate for the day
            - pageviews: Total pageviews for the day

    Example:
        >>> daily_engagement = get_engagement_by_date(traffic_df)
        >>> daily_engagement.plot(subplots=True)
    """
    return (
        df.groupby("date")
        .agg(
            {
                "session_duration": "mean",
                "bounce_rate": "mean",
                "pageviews": "sum",
            }
        )
        .reset_index()
    )


WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
MAD_SCALE = 0.6745
MIN_PERIODS = 7
MIN_SPREAD = 0.01


def filter_segments(
    df: pd.DataFrame,
    regions: list[str],
    devices: list[str],
    countries: list[str],
) -> pd.DataFrame:
    """Keep the rows that match the chosen regions, devices and countries.

    Args:
        df: Traffic data.
        regions: Regions to keep.
        devices: Devices to keep.
        countries: Countries to keep.

    Returns:
        The matching rows.
    """
    return df[
        df["region"].isin(regions)
        & df["device"].isin(devices)
        & df["country"].isin(countries)
    ]


def filter_frame(
    df: pd.DataFrame,
    start: pd.Timestamp,
    end: pd.Timestamp,
    regions: list[str],
    devices: list[str],
    countries: list[str],
) -> pd.DataFrame:
    """Keep the rows inside a date range that match the chosen segments.

    Args:
        df: Traffic data.
        start: First date to keep, inclusive.
        end: Last date to keep, inclusive.
        regions: Regions to keep.
        devices: Devices to keep.
        countries: Countries to keep.

    Returns:
        The matching rows.
    """
    dated = df[df["date"].between(start, end)]
    return filter_segments(dated, regions, devices, countries)


def resample_views(
    df: pd.DataFrame, freq: str, drop_partial: bool = True
) -> pd.DataFrame:
    """Total page views per day, week or month.

    A week or month that the data only partly covers would look like a sudden
    drop, so by default the final period is left out if it is incomplete.

    Args:
        df: Traffic data.
        freq: ``"D"`` for days, ``"W"`` for weeks or ``"MS"`` for months.
        drop_partial: Drop the last week or month if the data stops mid-period.

    Returns:
        Columns ``date`` and ``pageviews``, one row per period.
    """
    totals = df.groupby("date")["pageviews"].sum()
    if freq == "D":
        return totals.rename("pageviews").reset_index()
    periods = totals.resample(freq).sum()
    if drop_partial and len(periods):
        last_day = totals.index.max()
        offset = pd.tseries.frequencies.to_offset(freq)
        period_end = periods.index[-1] + offset - pd.Timedelta(days=1)
        if freq == "W":
            period_end = periods.index[-1]
        if last_day < period_end.normalize():
            periods = periods.iloc[:-1]
    return periods.rename("pageviews").reset_index()


def compact_number(value: float) -> str:
    """Shorten a large number for a headline figure.

    Args:
        value: Any non-negative number.

    Returns:
        For example ``842``, ``12.3k`` or ``142.9M``.
    """
    for threshold, divisor, suffix in (
        (1e9, 1e9, "B"),
        (1e6, 1e6, "M"),
        (1e4, 1e3, "k"),
    ):
        if value >= threshold:
            return f"{value / divisor:.1f}{suffix}"
    return f"{value:,.0f}"


def previous_period(
    df: pd.DataFrame, start: pd.Timestamp, end: pd.Timestamp
) -> pd.DataFrame:
    """Rows from the window of equal length immediately before ``start``.

    Args:
        df: Traffic data, before any date filtering.
        start: First date of the current window.
        end: Last date of the current window.

    Returns:
        The rows of the previous window, for comparing KPIs.
    """
    length = end - start + pd.Timedelta(days=1)
    return df[df["date"].between(start - length, start - pd.Timedelta(days=1))]


def percent_change(current: float, previous: float) -> float | None:
    """Percentage change from ``previous`` to ``current``.

    Args:
        current: The newer value.
        previous: The older value.

    Returns:
        The change in percent, or None when there is nothing to compare with.
    """
    if not previous:
        return None
    return float((current - previous) / previous * 100)


def weekday_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Average daily page views for each day of the week.

    Args:
        df: Traffic data.

    Returns:
        Columns ``weekday`` (Monday first) and ``pageviews``.
    """
    daily = df.groupby("date")["pageviews"].sum().reset_index()
    daily["weekday"] = daily["date"].dt.day_name()
    means = daily.groupby("weekday")["pageviews"].mean().reindex(WEEKDAYS)
    return means.rename("pageviews").reset_index()


def month_heatmap(df: pd.DataFrame) -> pd.DataFrame:
    """Total page views by year (rows) and calendar month (columns).

    Args:
        df: Traffic data.

    Returns:
        A pivot table with years down the side and months 1 to 12 across.
    """
    monthly = df.assign(year=df["date"].dt.year, month=df["date"].dt.month)
    return monthly.pivot_table(
        index="year", columns="month", values="pageviews", aggfunc="sum"
    ).reindex(columns=range(1, 13))


def rolling_anomalies(
    df: pd.DataFrame, window: int = 28, threshold: float = 3.5
) -> pd.DataFrame:
    """Flag days that are unusual compared with the days around them.

    The plain Z-score in :func:`detect_anomalies` judges every day against the
    whole period, so a steady upward trend makes the newest days look odd.
    This version measures each day against the median of the days around it
    (a centred window, so a rising trend leaves no lag) and scores the
    leftover with the median absolute deviation, which outliers cannot skew.

    Args:
        df: Traffic data.
        window: Trading days in the rolling median.
        threshold: Robust Z-score above which a day is flagged.

    Returns:
        Columns ``date``, ``pageviews``, ``expected`` and ``score`` for the
        flagged days only.
    """
    daily = df.groupby("date")["pageviews"].sum().reset_index()
    daily["expected"] = (
        daily["pageviews"]
        .rolling(window, center=True, min_periods=MIN_PERIODS)
        .median()
    )
    residual = daily["pageviews"] - daily["expected"]
    centre = residual.median()
    mad = (residual - centre).abs().median()
    # Without a floor, perfectly smooth data has zero spread and any wobble
    # would score as infinite. Treat 1% of typical traffic as the minimum spread.
    mad = max(mad, MIN_SPREAD * daily["pageviews"].median())
    if not mad:
        return daily.iloc[0:0].assign(score=pd.Series(dtype="float64"))
    daily["score"] = MAD_SCALE * (residual - centre) / mad
    return daily[daily["score"].abs() > threshold].reset_index(drop=True)
