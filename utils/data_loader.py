import pandas as pd
import streamlit as st
from pathlib import Path

@st.cache_data
def load_data(csv_file: Path) -> pd.DataFrame:
    """
    Load data from CSV file, parse dates, set index, and filter outliers.
    
    Args:
        csv_file (Path): Path to the CSV file.
        
    Returns:
        pd.DataFrame: Cleaned dataframe.
    """
    if not csv_file.exists():
        raise FileNotFoundError(f"File not found: {csv_file}")

    df = pd.read_csv(csv_file, parse_dates=["date"], index_col="date")
    
    # Clean data: keep values between 2.5th and 97.5th percentile
    lower_bound = df["value"].quantile(0.025)
    upper_bound = df["value"].quantile(0.975)
    
    df_cleaned = df[
        (df["value"] >= lower_bound) & 
        (df["value"] <= upper_bound)
    ]
    
    return df_cleaned.sort_index()
