"""
===================================================
Filename: main.py
Created Date: 24-02-2023
Author: Elliott Fairhall
Email: elliott@elliottfairhall.dev
Version: 1.5

Purpose:
--------
This script is designed to provide an interactive web application using Streamlit
for visualizing time-series data, specifically FreeCodeCamp forum page views.
The application allows users to choose different types of plots (line, bar, box)
and aggregation levels (day, month, year) for the data.

Revision History:
-----------------
24-03-2023: Added files to upload
01-03-2023: Inital project commit
08-04-2023: Cleaning code
05-08-2024: Implemented governance standards
===================================================
"""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pathlib import Path
from PIL import Image
from text_functions import (
    information_related_to_project_outline,
    information_on_time_series_data,
    show_line_chart_information,
    interactive_line_chart_title,
    static_bar_chart_title,
    show_bar_chart_information,
    box_chart_title,
    interactive_bar_chart_title,
    box_chart_information,
    line_chart_time_series_title,
)

PAGE_ICON = ":chart_with_upwards_trend:"
PAGE_TITLE = "Data Engineer, Educator Analyst and Technology Enthusiast"

# Set the title and icon of the application
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="centered")

# Set the path for the home page, csv file, and css file
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
home_page = current_dir / "Home_Page.py"
website_image = current_dir / "assets" / "images" / "Website.jpg"
csv_file = current_dir / "assets" / "data" / "fcc-forum-pageviews.csv"
css_file = current_dir / "styles" / "main.css"

# Read the css file and add it to the streamlit application
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

# Read the csv file and set the date column as the index
df = pd.read_csv(csv_file, parse_dates=["date"], index_col=["date"])

# Remove any outliers from the data keeping values within the 2.5 and 97.5 percentiles
df = df[
    (df["value"] >= df["value"].quantile(0.025))
    & (df["value"] <= df["value"].quantile(0.975))
]


def prepare_data(df):
    """Prepare the data for analysis."""
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Data must be a DataFrame")
    if "date" not in df.columns:
        raise ValueError("Dataframe must have a 'date' column")
    if "value" not in df.columns:
        raise ValueError("Dataframe must have a 'value' column")

    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    df.sort_index(inplace=True)
    return df


def draw_line_plot(df, title="Line Plot", xlabel="Date", ylabel="Page Views"):
    """Draw a line plot."""
    if df is None:
        raise ValueError("Dataframe is missing")
    fig, ax = plt.subplots()
    ax.plot(df.index, df["value"], "r", linewidth=1)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return fig


def draw_interactive_line_chart(df, aggregation_level):
    """Draw an interactive line chart."""
    if aggregation_level == "day":
        df.plot(kind="line", xlabel="date", ylabel="Page Views")
    elif aggregation_level == "month":
        df_month = df.resample("M").mean()
        df_month.plot(kind="line", xlabel="date", ylabel="Page Views")
    elif aggregation_level == "year":
        df_year = df.resample("Y").mean()
        df_year.plot(kind="line", xlabel="date", ylabel="Page Views")
    else:
        st.warning("Invalid aggregation level selected")
    plt.title("Daily freecodeCamp Forum Page Views")
    st.pyplot(plt.gcf())


def draw_bar_plot(df, title="Bar Plot", xlabel="Year", ylabel="Average Page Views"):
    """Draw a bar plot."""
    if df is None:
        raise ValueError("Dataframe is missing")
    df["month"] = df.index.month
    df["year"] = df.index.year
    df_bar = df.groupby(["year", "month"])["value"].mean()
    df_bar = df_bar.unstack()
    ax = df_bar.plot(kind="bar", stacked=True)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=0)
    plt.legend(
        [
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
    )
    for container in ax.containers:
        for bar in container:
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                bar.get_y() + bar.get_height() / 2.0,
                "%d" % int(bar.get_height()),
                ha="center",
                va="center",
                fontsize=6,
            )
    return plt


def draw_interactive_bar_chart(df, aggregation_level):
    """Draw an interactive bar chart."""
    if aggregation_level == "day":
        df.plot(kind="bar", xlabel="date", ylabel="Page Views")
    elif aggregation_level == "month":
        df_month = df.resample("M").mean()
        df_month.plot(kind="bar", xlabel="date", ylabel="Page Views")
    elif aggregation_level == "year":
        df_year = df.resample("Y").mean()
        df_year.plot(kind="bar", xlabel="date", ylabel="Page Views")
    else:
        st.warning("Invalid aggregation level selected")
    plt.title("Daily freecodeCamp Forum Page Views")
    st.pyplot(plt.gcf())


def draw_box_plot(
    df, title="Box and Whisker Plot", xlabel="Value", ylabel="Time Period"
):
    """Draw a box and whisker plot."""
    if df is None:
        raise ValueError("Dataframe is missing")
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")
    df_box["month_num"] = df_box["date"].dt.month
    df_box = df_box.sort_values("month_num")

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
    sns.boxplot(x="value", y="year", data=df_box, ax=axes[0])
    sns.boxplot(x="value", y="month", data=df_box, ax=axes[1])
    axes[0].set_title(f"{title} (Trend)")
    axes[0].set_xlabel(xlabel)
    axes[0].set_ylabel("Year")
    axes[1].set_title(f"{title} (Seasonality)")
    return fig


st.markdown(
    "<h1>Time-Series Analysis of FreeCodeCamp Forum Page Views</h1>",
    unsafe_allow_html=True,
)

st.markdown("## Project Outline")
information_related_to_project_outline()
st.markdown("---")

image = Image.open(website_image)
st.image(image, caption="Website Overview Image")
information_on_time_series_data()
st.markdown("---")

st.markdown("## Sample Data")
st.dataframe(df.head(5))
st.markdown("---")

st.markdown("## Data Information")
information_on_time_series_data()
st.markdown("---")

plot_type = st.selectbox("Select a chart type:", ["Line", "Bar", "Box"])
aggregation_level = st.selectbox(
    "Select the aggregation level:", ["day", "month", "year"]
)
st.markdown("---")

if plot_type == "Line":
    line_chart_time_series_title()
    st.pyplot(draw_line_plot(df))
    show_line_chart_information()
    interactive_line_chart_title()
    draw_interactive_line_chart(df, aggregation_level)
elif plot_type == "Bar":
    static_bar_chart_title()
    st.pyplot(draw_bar_plot(df))
    show_bar_chart_information()
    interactive_bar_chart_title()
    draw_interactive_bar_chart(df, aggregation_level)
else:
    box_chart_title()
    st.pyplot(draw_box_plot(df))
    box_chart_information()

st.markdown("---")