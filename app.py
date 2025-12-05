import streamlit as st
from pathlib import Path

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Page Views Analysis", 
    page_icon=":chart_with_upwards_trend:", 
    layout="wide"
)

from utils.data_loader import load_data
from utils.plots import (
    draw_line_plot, 
    draw_bar_plot, 
    draw_box_plot, 
    draw_interactive_line_chart, 
    draw_interactive_bar_chart
)
import utils.text as text

# --- Constants ---
CURRENT_DIR = Path(__file__).parent
CSV_FILE = CURRENT_DIR / "assets" / "data" / "fcc-forum-pageviews.csv"
CSS_FILE = CURRENT_DIR / "styles" / "main.css"

# --- Setup ---
def load_css(file_path):
    if file_path.exists():
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css(CSS_FILE)

# --- Main App ---
def main():
    st.title("FreeCodeCamp Forum Page Views Analysis")
    
    # 1. Overview
    text.project_overview()
    st.markdown("---")

    # 2. Data Loading
    try:
        df = load_data(CSV_FILE)
    except FileNotFoundError:
        st.error(f"Data file not found at {CSV_FILE}. Please checks assets.")
        return

    # 3. Data Preview
    with st.expander("View Raw Data"):
        st.dataframe(df.head())
        text.time_series_info()
    st.markdown("---")

    # 4. Interactive Controls
    st.sidebar.header("Configuration")
    plot_type = st.sidebar.selectbox("Choose Chart Type", ["Line Plot", "Bar Plot", "Box Plot"])
    
    # Aggregation is only relevant for interactive charts if we want to keep that logic,
    # but based on the original app, it had a specific flow. Let's keep it simple and powerful.
    
    if plot_type == "Line Plot":
        text.line_chart_info()
        st.pyplot(draw_line_plot(df))
        
        st.subheader("Interactive Line Chart")
        agg = st.selectbox("Aggregation Level", ["Day", "Month", "Year"], key="line_agg")
        draw_interactive_line_chart(df, agg)

    elif plot_type == "Bar Plot":
        text.bar_chart_info()
        st.pyplot(draw_bar_plot(df))
        
        st.subheader("Interactive Bar Chart")
        agg = st.selectbox("Aggregation Level", ["Day", "Month", "Year"], key="bar_agg")
        draw_interactive_bar_chart(df, agg)

    elif plot_type == "Box Plot":
        text.box_chart_info()
        st.pyplot(draw_box_plot(df))

if __name__ == "__main__":
    main()
