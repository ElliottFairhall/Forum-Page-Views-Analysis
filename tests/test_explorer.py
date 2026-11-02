"""Tests for the explorer's analytics and the live page."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from utils.analytics import (
    WEEKDAYS,
    compact_number,
    filter_frame,
    filter_segments,
    month_heatmap,
    percent_change,
    previous_period,
    resample_views,
    rolling_anomalies,
    weekday_profile,
)

ROOT = Path(__file__).resolve().parent.parent


def _frame(days: int = 120, spike_on: int | None = None) -> pd.DataFrame:
    """Two countries, two devices, a steady upward trend and an optional spike."""
    rows = []
    for offset, date in enumerate(pd.date_range("2025-01-01", periods=days)):
        for country, region in (("France", "Europe"), ("Japan", "Asia")):
            for device in ("Desktop", "Mobile"):
                views = 100 + offset
                if spike_on is not None and offset == spike_on:
                    views *= 8
                rows.append((date, views, country, "XXX", region, device, 90.0, 0.4))
    return pd.DataFrame(
        rows,
        columns=[
            "date",
            "pageviews",
            "country",
            "iso_code",
            "region",
            "device",
            "session_duration",
            "bounce_rate",
        ],
    )


def test_segment_filters_keep_only_matches() -> None:
    """Region, device and country filters combine with AND."""
    df = _frame()
    kept = filter_segments(df, ["Europe"], ["Mobile"], ["France", "Japan"])
    assert set(kept["country"]) == {"France"}
    assert set(kept["device"]) == {"Mobile"}


def test_date_filter_is_inclusive() -> None:
    """Both end dates are included."""
    df = _frame()
    start, end = pd.Timestamp("2025-01-10"), pd.Timestamp("2025-01-12")
    kept = filter_frame(
        df, start, end, ["Europe", "Asia"], ["Desktop", "Mobile"], ["France", "Japan"]
    )
    assert kept["date"].min() == start
    assert kept["date"].max() == end


def test_previous_period_has_the_same_length() -> None:
    """The comparison window is as long as the current one and ends the day before."""
    df = _frame()
    start, end = pd.Timestamp("2025-02-01"), pd.Timestamp("2025-02-10")
    before = previous_period(df, start, end)
    assert before["date"].nunique() == 10
    assert before["date"].max() == pd.Timestamp("2025-01-31")


def test_percent_change_handles_zero_and_normal_cases() -> None:
    """Nothing to compare with gives None, not a division error."""
    assert percent_change(110, 100) == pytest.approx(10.0)
    assert percent_change(5, 0) is None


@pytest.mark.parametrize(
    ("value", "expected"),
    [(842, "842"), (12_345, "12.3k"), (142_887_000, "142.9M"), (2_100_000_000, "2.1B")],
)
def test_compact_number(value: float, expected: str) -> None:
    """Large headline figures are shortened."""
    assert compact_number(value) == expected


def test_resample_by_day_week_and_month() -> None:
    """Totals add up whatever the granularity."""
    df = _frame(days=60)
    total = df["pageviews"].sum()
    for freq in ("D", "W", "MS"):
        assert resample_views(df, freq, drop_partial=False)["pageviews"].sum() == total


def test_partial_trailing_period_is_dropped() -> None:
    """Data ending mid-week or mid-month must not end on a misleading dip."""
    df = _frame(days=60)  # ends 1 March 2025, a Saturday
    weekly = resample_views(df, "W")
    assert weekly["date"].max() < df["date"].max()
    assert weekly["date"].max().weekday() == 6  # a complete week ends on Sunday
    monthly = resample_views(df, "MS")
    assert monthly["date"].tolist() == [
        pd.Timestamp("2025-01-01"),
        pd.Timestamp("2025-02-01"),
    ]  # March holds one day only


def test_weekday_profile_is_in_calendar_order() -> None:
    """Monday first, seven rows."""
    profile = weekday_profile(_frame())
    assert profile["weekday"].tolist() == WEEKDAYS


def test_month_heatmap_always_has_twelve_months() -> None:
    """Missing months show as gaps rather than shifting the columns."""
    pivot = month_heatmap(_frame(days=60))
    assert list(pivot.columns) == list(range(1, 13))
    assert pivot[1].notna().all()
    assert pivot[12].isna().all()


def test_rolling_detector_ignores_a_steady_trend() -> None:
    """A smooth climb is not unusual; the old whole-period Z-score would flag it."""
    assert rolling_anomalies(_frame(days=300)).empty


def test_rolling_detector_finds_a_spike() -> None:
    """A day with eight times the usual views is flagged, and only that day."""
    found = rolling_anomalies(_frame(days=120, spike_on=80))
    assert found["date"].tolist() == [
        pd.Timestamp("2025-01-01") + pd.Timedelta(days=80)
    ]
    assert found["score"].iloc[0] > 0


def test_rolling_detector_copes_with_flat_data() -> None:
    """Zero variation means nothing to flag, never a divide-by-zero."""
    df = _frame(days=40)
    df["pageviews"] = 100
    assert rolling_anomalies(df).empty


def _run() -> AppTest:
    return AppTest.from_file(str(ROOT / "app.py"), default_timeout=120).run()


def test_page_renders_with_four_metrics_and_deltas() -> None:
    """The opening state shows the KPIs, each compared with the prior period."""
    at = _run()
    assert not at.exception, [e.value for e in at.exception]
    assert [m.label for m in at.metric] == [
        "Page views",
        "Average per day",
        "Session length",
        "Bounce rate",
    ]
    assert any("synthetic" in c.value.lower() for c in at.caption)


def test_device_filter_changes_the_numbers() -> None:
    """Dropping devices lowers total page views."""
    full = _run()
    total_full = full.metric[1].value
    full.multiselect(key="devices").set_value(["Desktop"]).run()
    assert not full.exception
    assert full.metric[1].value != total_full


def test_region_filter_narrows_the_country_list() -> None:
    """Choosing one region leaves only its countries to pick from."""
    at = _run()
    at.multiselect(key="regions").set_value(["Europe"]).run()
    assert not at.exception
    assert 0 < len(at.multiselect(key="countries").options) < 13


def test_empty_selection_warns_instead_of_failing() -> None:
    """With no devices chosen the page says so."""
    at = _run()
    at.multiselect(key="devices").set_value([]).run()
    assert not at.exception
    assert any("Nothing matches" in w.value for w in at.warning)


def test_every_granularity_renders() -> None:
    """Day, Week and Month all draw without error."""
    for choice in ("Day", "Month"):
        at = _run()
        control = next(
            c
            for c in at.get("segmented_control")
            if getattr(c, "label", "") == "Trend by"
        )
        control.set_value(choice).run()
        assert not at.exception, choice


def test_synthetic_data_is_the_expected_size() -> None:
    """Guard the bundled dataset: ten years, thirteen countries."""
    df = pd.read_csv(
        ROOT / "assets" / "data" / "platform-traffic.csv", parse_dates=["date"]
    )
    assert df["country"].nunique() == 13
    assert (df["date"].max() - df["date"].min()).days > 3000
    assert np.isfinite(df["pageviews"]).all()
