"""Synthetic traffic data generator for the Intelligence Flux dashboard.

This module generates realistic multi-dimensional web traffic data with
temporal patterns including growth trends, seasonality, and random spikes.
"""

import argparse
import logging
import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def generate_synthetic_data(
    start_date: str = "2016-05-09",
    end_date: str = "2026-01-31",
    output_path: Path | None = None,
) -> pd.DataFrame:
    """Generate multi-dimensional synthetic traffic data.

    Args:
        start_date: Start date in YYYY-MM-DD format.
        end_date: End date in YYYY-MM-DD format.
        output_path: Optional path to save CSV. If None, uses default location.

    Returns:
        DataFrame containing synthetic traffic data with columns:
        date, pageviews, country, iso_code, region, device,
        session_duration, bounce_rate.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end - start
    days = delta.days + 1
    dates = [start + timedelta(days=i) for i in range(days)]

    t = np.arange(days)
    growth = 1000 + 10 * t + 0.005 * (t**2)
    seasonality = 500 * np.sin(2 * np.pi * t / 365.25)
    weekly = 200 * np.sin(2 * np.pi * t / 7)
    noise = np.random.normal(0, 300, days)
    pageviews = np.maximum(500, (growth + seasonality + weekly + noise).astype(int))

    spike_indices = np.random.choice(days, size=15, replace=False)
    for idx in spike_indices:
        pageviews[idx] *= np.random.uniform(2, 4)

    df_base = pd.DataFrame({"date": dates, "pageviews": pageviews})

    country_pool = [
        {"name": "United States", "iso": "USA", "region": "North America"},
        {"name": "Canada", "iso": "CAN", "region": "North America"},
        {"name": "United Kingdom", "iso": "GBR", "region": "Europe"},
        {"name": "Germany", "iso": "DEU", "region": "Europe"},
        {"name": "France", "iso": "FRA", "region": "Europe"},
        {"name": "India", "iso": "IND", "region": "Asia"},
        {"name": "Japan", "iso": "JPN", "region": "Asia"},
        {"name": "Australia", "iso": "AUS", "region": "Oceania"},
        {"name": "Brazil", "iso": "BRA", "region": "South America"},
        {"name": "Nigeria", "iso": "NGA", "region": "Africa"},
        {"name": "Mexico", "iso": "MEX", "region": "North America"},
        {"name": "China", "iso": "CHN", "region": "Asia"},
        {"name": "South Africa", "iso": "ZAF", "region": "Africa"},
    ]
    devices = ["Desktop", "Mobile", "Tablet"]

    granular_data = []
    for d in dates:
        num_segments = np.random.randint(5, 12)
        daily_views = df_base[df_base["date"] == d]["pageviews"].values[0]
        weights = np.random.dirichlet(np.ones(num_segments))
        segment_views = (weights * daily_views).astype(int)

        for i in range(num_segments):
            c = random.choice(country_pool)
            device = np.random.choice(devices, p=[0.5, 0.4, 0.1])
            # Clamp duration to positive values (minimum 5 seconds)
            base_duration = 120 if device == "Desktop" else 80
            std_duration = 30 if device == "Desktop" else 40
            avg_duration = max(5.0, np.random.normal(base_duration, std_duration))
            bounce_rate = np.random.uniform(0.2, 0.5)

            granular_data.append(
                {
                    "date": d.strftime("%Y-%m-%d"),
                    "pageviews": segment_views[i],
                    "country": c["name"],
                    "iso_code": c["iso"],
                    "region": c["region"],
                    "device": device,
                    "session_duration": round(avg_duration, 2),
                    "bounce_rate": round(bounce_rate, 4),
                }
            )

    final_df = pd.DataFrame(granular_data)

    if output_path is None:
        # Default to project's assets/data directory
        script_dir = Path(__file__).parent
        output_path = script_dir.parent / "assets" / "data" / "platform-traffic.csv"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(output_path, index=False)
    logger.info("Generated %d rows of data to %s", len(final_df), output_path)

    return final_df


def main() -> None:
    """CLI entry point for data synthesis."""
    parser = argparse.ArgumentParser(
        description="Generate synthetic platform traffic data"
    )
    parser.add_argument(
        "--start-date",
        default="2016-05-09",
        help="Start date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--end-date",
        default="2026-01-31",
        help="End date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output CSV path (default: assets/data/platform-traffic.csv)",
    )
    args = parser.parse_args()

    generate_synthetic_data(
        start_date=args.start_date,
        end_date=args.end_date,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()
