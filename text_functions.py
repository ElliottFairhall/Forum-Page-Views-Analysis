# ===================================================
# Filename: text_functions.py
# Created Date: 08-04-2023
# Author: Elliott Fairhall
# Email: elliott@elliottfairhall.dev
# Version: 2.0
#
# Purpose:
# --------
# Streamlit text sections used in the time-series app.
#
# Revision History:
# -----------------
# 08-04-2023: Cleaning code
# 05-08-2024: Implemented governance standards
# 05-09-2025: Content/style cleanup, consistency, DRY
# ===================================================

import streamlit as st

# --- small helpers ------------------------------------------------------------

def _section(title: str, body_md: str, level: int = 2):
    """Render a Markdown section with consistent heading level."""
    hash_marks = "#" * max(1, min(level, 6))
    st.markdown(f"{hash_marks} {title}")
    if body_md.strip():
        st.markdown(body_md)

def _bullets(items):
    return "\n".join([f"- {it}" for it in items])

# --- content sections ---------------------------------------------------------

def information_related_to_project_outline():
    _section(
        "Project Overview",
        """
This project visualizes **daily page views** on the **freeCodeCamp Forum** from May 2016 to December 2019.

You can explore the data with three chart types:

- **Line chart** – daily views over time (good for overall trend and changes).
- **Bar chart** – average **monthly** views per year (good for comparing seasonality across years).
- **Box & whisker** – distribution by **year** (trend) and by **month** (seasonality).

The dataset is loaded from CSV and lightly cleaned (e.g., outlier clipping) for clearer visuals.
        """,
        level=2,
    )


def time_series_data_summary():
    _section(
        "Time-Series Data Summary",
        """
The dataset is a **daily time series** with two columns:

- `date` — ISO-like date string (e.g., `YYYY-MM-DDT00:00:00`)
- `value` — number of page views for that day

Typical analyses include trend and seasonality detection, spotting spikes/dips (events, releases, promotions), and grouping by periods (weekdays, months, holidays). You can also compare against external drivers (e.g., campaigns or macro events) to understand impact on traffic.
        """,
        level=2,
    )


def information_on_time_series_data():
    _section(
        "Chart Type",
        """
Use the controls to pick a **chart** and an **aggregation** level (**day**, **month**, **year**).  
The interactive example below the static chart reflects your selections and is intended to help compare periods cleanly.
        """,
        level=2,
    )


def show_line_chart_information():
    _section(
        "Line Charts",
        _bullets([
            "Great for showing **trend**, **seasonality**, and **level shifts** over time.",
            "Easy to read when sampling is regular (daily) and density is reasonable.",
            "Overlaying a rolling mean can clarify trend without hiding variability.",
        ])
        + """

**Limitations**

- Less effective for showing **distribution**; dense series can look cluttered.
        """,
        level=2,
    )


def show_bar_chart_information():
    _section(
        "Bar Charts",
        _bullets([
            "Useful for comparing **aggregated** values (e.g., average monthly views) across **years**.",
            "Highlights **seasonal patterns** by month when grouped by year.",
            "Good for presentations where exact distributions are less important than comparisons.",
        ])
        + """

**Limitations**

- Can mislead if the y-axis doesn’t start at 0 or if bars represent irregular time spans.
        """,
        level=2,
    )


def _boxplot_shared_body():
    return """
**What it shows**

- The distribution by **year** (long-term trend) and by **month** (seasonality).
- **Median**, **IQR**, and **outliers**, helping you spot unusual periods quickly.

**Why it helps**

- Disentangles trend vs seasonality without committing to a specific model.
- Robust to extreme values compared with mean-based summaries.
    """


def show_box_chart_information():
    # Backward-compatible name retained, content de-duplicated & corrected
    _section("Box & Whisker Plots", _boxplot_shared_body(), level=2)


def box_chart_information():
    # This previously duplicated similar content; keep alias for compatibility.
    show_box_chart_information()


def interactive_line_chart_title():
    _section("Interactive Line Chart", "", level=1)


def static_bar_chart_title():
    _section("Reasons for Using Bar Charts with Time-Series Data", "", level=1)


def box_chart_title():
    _section("Reasons for Using Box & Whisker Plots with Time-Series Data", "", level=1)


def interactive_bar_chart_title():
    _section("Interactive Bar Chart", "", level=1)


def line_chart_time_series_title():
    _section("Reasons for Using Line Charts with Time-Series Data", "", level=1)
