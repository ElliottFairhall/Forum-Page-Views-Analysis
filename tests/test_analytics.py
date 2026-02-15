"""Unit tests for the analytics module."""

import numpy as np
import pandas as pd
import pytest

from utils.analytics import (
    detect_anomalies,
    get_audience_breakdown,
    get_engagement_by_date,
    get_kpis,
)


@pytest.fixture
def sample_traffic_data() -> pd.DataFrame:
    """Create sample traffic data for testing."""
    dates = pd.date_range(start="2024-01-01", periods=30, freq="D")
    data = []

    for date in dates:
        # Create multiple records per day
        for _ in range(5):
            data.append(
                {
                    "date": date,
                    "pageviews": np.random.randint(100, 1000),
                    "country": np.random.choice(["USA", "UK", "Germany"]),
                    "iso_code": np.random.choice(["USA", "GBR", "DEU"]),
                    "region": np.random.choice(["North America", "Europe"]),
                    "device": np.random.choice(["Desktop", "Mobile", "Tablet"]),
                    "session_duration": np.random.uniform(60, 180),
                    "bounce_rate": np.random.uniform(0.2, 0.5),
                }
            )

    return pd.DataFrame(data)


@pytest.fixture
def anomaly_data() -> pd.DataFrame:
    """Create data with known anomalies for testing."""
    dates = pd.date_range(start="2024-01-01", periods=30, freq="D")
    pageviews = [500] * 30  # Normal baseline

    # Add known anomalies
    pageviews[10] = 5000  # Spike
    pageviews[20] = 50  # Dip

    return pd.DataFrame({"date": dates, "pageviews": pageviews})


class TestGetKpis:
    """Tests for the get_kpis function."""

    def test_returns_dict_with_expected_keys(
        self, sample_traffic_data: pd.DataFrame
    ) -> None:
        """Test that get_kpis returns all expected keys."""
        kpis = get_kpis(sample_traffic_data)

        assert "total_views" in kpis
        assert "avg_daily_views" in kpis
        assert "avg_session" in kpis
        assert "avg_bounce" in kpis

    def test_total_views_is_positive(self, sample_traffic_data: pd.DataFrame) -> None:
        """Test that total views is a positive integer."""
        kpis = get_kpis(sample_traffic_data)

        assert isinstance(kpis["total_views"], int)
        assert kpis["total_views"] > 0

    def test_avg_daily_views_calculation(self) -> None:
        """Test average daily views calculation with known data."""
        df = pd.DataFrame(
            {
                "date": pd.to_datetime(["2024-01-01", "2024-01-01", "2024-01-02"]),
                "pageviews": [100, 200, 300],
                "session_duration": [60, 60, 60],
                "bounce_rate": [0.3, 0.3, 0.3],
            }
        )
        kpis = get_kpis(df)

        # Day 1: 300, Day 2: 300 -> avg = 300
        assert kpis["avg_daily_views"] == 300

    def test_bounce_rate_is_decimal(self, sample_traffic_data: pd.DataFrame) -> None:
        """Test that bounce rate is returned as a decimal between 0 and 1."""
        kpis = get_kpis(sample_traffic_data)

        assert 0 <= kpis["avg_bounce"] <= 1


class TestDetectAnomalies:
    """Tests for the detect_anomalies function."""

    def test_returns_dataframe(self, sample_traffic_data: pd.DataFrame) -> None:
        """Test that detect_anomalies returns a DataFrame."""
        result = detect_anomalies(sample_traffic_data)
        assert isinstance(result, pd.DataFrame)

    def test_detects_known_anomalies(self, anomaly_data: pd.DataFrame) -> None:
        """Test that obvious outliers are detected."""
        result = detect_anomalies(anomaly_data, threshold=2.0)

        # Should detect the spike day
        assert len(result) >= 1

    def test_higher_threshold_fewer_anomalies(
        self, sample_traffic_data: pd.DataFrame
    ) -> None:
        """Test that higher threshold detects fewer anomalies."""
        low_threshold = detect_anomalies(sample_traffic_data, threshold=1.5)
        high_threshold = detect_anomalies(sample_traffic_data, threshold=3.0)

        assert len(high_threshold) <= len(low_threshold)

    def test_result_has_is_anomaly_column(
        self, sample_traffic_data: pd.DataFrame
    ) -> None:
        """Test that result contains is_anomaly column."""
        result = detect_anomalies(sample_traffic_data)

        if len(result) > 0:
            assert "is_anomaly" in result.columns
            assert result["is_anomaly"].all()  # All returned rows are anomalies


class TestGetAudienceBreakdown:
    """Tests for the get_audience_breakdown function."""

    def test_returns_dataframe(self, sample_traffic_data: pd.DataFrame) -> None:
        """Test that function returns a DataFrame."""
        result = get_audience_breakdown(sample_traffic_data, dimension="device")
        assert isinstance(result, pd.DataFrame)

    def test_aggregates_by_device(self, sample_traffic_data: pd.DataFrame) -> None:
        """Test aggregation by device dimension."""
        result = get_audience_breakdown(sample_traffic_data, dimension="device")

        assert "device" in result.columns
        assert "pageviews" in result.columns
        assert len(result) <= 3  # Desktop, Mobile, Tablet

    def test_aggregates_by_region(self, sample_traffic_data: pd.DataFrame) -> None:
        """Test aggregation by region dimension."""
        result = get_audience_breakdown(sample_traffic_data, dimension="region")

        assert "region" in result.columns
        assert len(result) <= 2  # North America, Europe

    def test_raises_error_for_invalid_dimension(
        self, sample_traffic_data: pd.DataFrame
    ) -> None:
        """Test that invalid dimension raises KeyError."""
        with pytest.raises(KeyError, match="not found"):
            get_audience_breakdown(sample_traffic_data, dimension="nonexistent")

    def test_total_matches_source(self, sample_traffic_data: pd.DataFrame) -> None:
        """Test that aggregated total matches source total."""
        result = get_audience_breakdown(sample_traffic_data, dimension="device")

        assert result["pageviews"].sum() == sample_traffic_data["pageviews"].sum()


class TestGetEngagementByDate:
    """Tests for the get_engagement_by_date function."""

    def test_returns_dataframe(self, sample_traffic_data: pd.DataFrame) -> None:
        """Test that function returns a DataFrame."""
        result = get_engagement_by_date(sample_traffic_data)
        assert isinstance(result, pd.DataFrame)

    def test_has_expected_columns(self, sample_traffic_data: pd.DataFrame) -> None:
        """Test that result has expected columns."""
        result = get_engagement_by_date(sample_traffic_data)

        assert "date" in result.columns
        assert "session_duration" in result.columns
        assert "bounce_rate" in result.columns
        assert "pageviews" in result.columns

    def test_aggregation_correct(self) -> None:
        """Test that aggregation is correct with known data."""
        df = pd.DataFrame(
            {
                "date": pd.to_datetime(["2024-01-01", "2024-01-01"]),
                "session_duration": [60, 120],
                "bounce_rate": [0.2, 0.4],
                "pageviews": [100, 200],
            }
        )
        result = get_engagement_by_date(df)

        assert len(result) == 1
        assert result.iloc[0]["session_duration"] == pytest.approx(90)  # mean
        assert result.iloc[0]["bounce_rate"] == pytest.approx(0.3)  # mean
        assert result.iloc[0]["pageviews"] == 300  # sum

    def test_one_row_per_date(self, sample_traffic_data: pd.DataFrame) -> None:
        """Test that result has one row per unique date."""
        result = get_engagement_by_date(sample_traffic_data)
        unique_dates = sample_traffic_data["date"].nunique()

        assert len(result) == unique_dates
