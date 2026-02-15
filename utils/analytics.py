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
