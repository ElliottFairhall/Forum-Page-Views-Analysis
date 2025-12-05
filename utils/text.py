import streamlit as st

def _section_header(title: str):
    st.markdown(f"## {title}")

def project_overview():
    _section_header("Project Overview")
    st.markdown("""
    This project visualizes **daily page views** on the **freeCodeCamp Forum**.
    
    - **Line chart**: Daily views over time (Trend/Noise).
    - **Bar chart**: Average monthly views per year (Seasonality/Comparison).
    - **Box & Whisker**: Distribution by year and month (Outliers/Spread).
    """)

def time_series_info():
    _section_header("Time-Series Data Info")
    st.info("""
    The dataset contains daily page views. 
    Analysis of this data helps in understanding traffic trends, seasonal patterns, and growth over time.
    """)

def line_chart_info():
    st.markdown("""
    ### Line Charts
    - Show trends and changes over time.
    - Good for identifying overall growth or decline.
    """)

def bar_chart_info():
    st.markdown("""
    ### Bar Charts
    - Compare categories or aggregated time periods.
    - Here, we compare months across different years to see seasonal consistencies.
    """)

def box_chart_info():
    st.markdown("""
    ### Box Plots
    - **Year-wise**: Shows the trend of distributions over years.
    - **Month-wise**: Shows seasonal distributions (e.g., is traffic consistently higher in October?).
    - Points outside the 'whiskers' are **outliers**.
    """)
