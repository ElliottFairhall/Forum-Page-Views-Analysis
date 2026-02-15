"""Unit tests for the data_loader module."""

import tempfile
from pathlib import Path

import pandas as pd
import pytest

from utils.data_loader import load_source_data, validate_data_quality


@pytest.fixture
def valid_csv_file() -> Path:
    """Create a temporary valid CSV file for testing."""
    content = """date,pageviews,country,iso_code,region,device,session_duration,bounce_rate
2024-01-01,100,USA,USA,North America,Desktop,120.5,0.35
2024-01-02,200,UK,GBR,Europe,Mobile,80.0,0.45
2024-01-03,150,Germany,DEU,Europe,Tablet,100.0,0.30"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(content)
        return Path(f.name)


@pytest.fixture
def missing_columns_csv() -> Path:
    """Create a CSV file with missing required columns."""
    content = """date,pageviews,country
2024-01-01,100,USA"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(content)
        return Path(f.name)


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """Create a sample DataFrame for quality validation tests."""
    return pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "pageviews": [100, 200],
            "country": ["USA", "UK"],
            "iso_code": ["USA", "GBR"],
            "region": ["North America", "Europe"],
            "device": ["Desktop", "Mobile"],
            "session_duration": [120.0, 80.0],
            "bounce_rate": [0.35, 0.45],
        }
    )


class TestLoadSourceData:
    """Tests for the load_source_data function."""

    def test_loads_valid_csv(self, valid_csv_file: Path) -> None:
        """Test that valid CSV is loaded correctly."""
        df = load_source_data(valid_csv_file)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3

    def test_parses_date_column(self, valid_csv_file: Path) -> None:
        """Test that date column is parsed as datetime."""
        df = load_source_data(valid_csv_file)

        assert pd.api.types.is_datetime64_any_dtype(df["date"])

    def test_returns_sorted_by_date(self, valid_csv_file: Path) -> None:
        """Test that returned DataFrame is sorted by date."""
        df = load_source_data(valid_csv_file)

        assert df["date"].is_monotonic_increasing

    def test_raises_file_not_found(self) -> None:
        """Test that FileNotFoundError is raised for missing file."""
        with pytest.raises(FileNotFoundError, match="Data file not found"):
            load_source_data(Path("/nonexistent/path/file.csv"))

    def test_raises_value_error_missing_columns(
        self, missing_columns_csv: Path
    ) -> None:
        """Test that ValueError is raised when columns are missing."""
        with pytest.raises(ValueError, match="Missing required columns"):
            load_source_data(missing_columns_csv)

    def test_accepts_string_path(self, valid_csv_file: Path) -> None:
        """Test that function accepts string path as well as Path."""
        df = load_source_data(str(valid_csv_file))
        assert isinstance(df, pd.DataFrame)


class TestValidateDataQuality:
    """Tests for the validate_data_quality function."""

    def test_returns_dict(self, sample_dataframe: pd.DataFrame) -> None:
        """Test that function returns a dictionary."""
        result = validate_data_quality(sample_dataframe)
        assert isinstance(result, dict)

    def test_valid_data_passes_all_checks(self, sample_dataframe: pd.DataFrame) -> None:
        """Test that valid data passes all quality checks."""
        result = validate_data_quality(sample_dataframe)

        assert result["no_nulls"]
        assert result["positive_pageviews"]
        assert result["valid_bounce_rates"]
        assert result["positive_duration"]

    def test_detects_null_values(self) -> None:
        """Test that null values are detected."""
        df = pd.DataFrame(
            {
                "date": [pd.Timestamp("2024-01-01"), None],
                "pageviews": [100, 200],
                "country": ["USA", "UK"],
                "iso_code": ["USA", "GBR"],
                "region": ["North America", "Europe"],
                "device": ["Desktop", "Mobile"],
                "session_duration": [120.0, 80.0],
                "bounce_rate": [0.35, 0.45],
            }
        )
        result = validate_data_quality(df)

        assert not result["no_nulls"]

    def test_detects_negative_pageviews(self) -> None:
        """Test that negative pageviews are detected."""
        df = pd.DataFrame(
            {
                "date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
                "pageviews": [-100, 200],
                "country": ["USA", "UK"],
                "iso_code": ["USA", "GBR"],
                "region": ["North America", "Europe"],
                "device": ["Desktop", "Mobile"],
                "session_duration": [120.0, 80.0],
                "bounce_rate": [0.35, 0.45],
            }
        )
        result = validate_data_quality(df)

        assert not result["positive_pageviews"]

    def test_detects_invalid_bounce_rates(self) -> None:
        """Test that bounce rates outside 0-1 are detected."""
        df = pd.DataFrame(
            {
                "date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
                "pageviews": [100, 200],
                "country": ["USA", "UK"],
                "iso_code": ["USA", "GBR"],
                "region": ["North America", "Europe"],
                "device": ["Desktop", "Mobile"],
                "session_duration": [120.0, 80.0],
                "bounce_rate": [0.35, 1.5],  # Invalid: > 1
            }
        )
        result = validate_data_quality(df)

        assert not result["valid_bounce_rates"]

    def test_detects_negative_duration(self) -> None:
        """Test that negative session durations are detected."""
        df = pd.DataFrame(
            {
                "date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
                "pageviews": [100, 200],
                "country": ["USA", "UK"],
                "iso_code": ["USA", "GBR"],
                "region": ["North America", "Europe"],
                "device": ["Desktop", "Mobile"],
                "session_duration": [-5.0, 80.0],  # Invalid: negative
                "bounce_rate": [0.35, 0.45],
            }
        )
        result = validate_data_quality(df)

        assert not result["positive_duration"]
