"""Data loading utilities for the Intelligence Flux dashboard.

This module handles loading and validating traffic data from CSV files.
"""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def load_source_data(csv_file: Path | str) -> pd.DataFrame:
    """Load platform traffic data from a CSV file.

    Reads the traffic data CSV, parses date columns, and performs
    basic validation to ensure data quality.

    Args:
        csv_file: Path to the CSV file containing traffic data.
            Can be a Path object or string path.

    Returns:
        DataFrame sorted by date with columns:
            - date: Datetime column
            - pageviews: Integer page view counts
            - country: Country name
            - iso_code: ISO 3166-1 alpha-3 country code
            - region: Geographic region
            - device: Device type (Desktop, Mobile, Tablet)
            - session_duration: Session length in seconds
            - bounce_rate: Bounce rate (0-1)

    Raises:
        FileNotFoundError: If the specified CSV file does not exist.
        ValueError: If required columns are missing from the file.

    Example:
        >>> from pathlib import Path
        >>> df = load_source_data(Path("assets/data/platform-traffic.csv"))
        >>> print(f"Loaded {len(df)} records from {df['date'].min()} to {df['date'].max()}")
    """
    csv_path = Path(csv_file)

    if not csv_path.exists():
        raise FileNotFoundError(f"Data file not found: {csv_path}")

    df = pd.read_csv(csv_path, parse_dates=["date"])
    df["date"] = pd.to_datetime(df["date"])

    # Validate required columns
    required_columns = {
        "date",
        "pageviews",
        "country",
        "iso_code",
        "region",
        "device",
        "session_duration",
        "bounce_rate",
    }
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Log data summary
    logger.info(
        "Loaded %d records spanning %s to %s",
        len(df),
        df["date"].min().strftime("%Y-%m-%d"),
        df["date"].max().strftime("%Y-%m-%d"),
    )

    return df.sort_values("date")


def validate_data_quality(df: pd.DataFrame) -> dict[str, bool]:
    """Validate data quality and return a summary of checks.

    Performs quality checks on the loaded traffic data to identify
    potential issues.

    Args:
        df: DataFrame to validate.

    Returns:
        Dictionary with quality check results:
            - no_nulls: True if no null values exist
            - positive_pageviews: True if all pageviews are positive
            - valid_bounce_rates: True if all bounce rates are between 0 and 1
            - positive_duration: True if all session durations are positive

    Example:
        >>> quality = validate_data_quality(df)
        >>> if not all(quality.values()):
        ...     print("Data quality issues detected!")
    """
    return {
        "no_nulls": not df.isnull().any().any(),
        "positive_pageviews": (df["pageviews"] >= 0).all(),
        "valid_bounce_rates": (
            (df["bounce_rate"] >= 0) & (df["bounce_rate"] <= 1)
        ).all(),
        "positive_duration": (df["session_duration"] > 0).all(),
    }
