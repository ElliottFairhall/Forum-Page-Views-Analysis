import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st

def draw_line_plot(df: pd.DataFrame, title: str = "Daily freeCodeCamp Forum Page Views 5/2016-12/2019", xlabel: str = "Date", ylabel: str = "Page Views") -> plt.Figure:
    """Draw a static line plot."""
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df["value"], "r", linewidth=1)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return fig

def draw_bar_plot(df: pd.DataFrame, title: str = "Average Page Views per Year", xlabel: str = "Years", ylabel: str = "Average Page Views") -> plt.Figure:
    """Draw a bar plot showing average daily page views for each month grouped by year."""
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month_name()
    
    # Order months correctly
    month_order = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(
        data=df_bar, 
        x="year", 
        y="value", 
        hue="month", 
        hue_order=month_order,
        palette="tab10",
        errorbar=None,
        ax=ax
    )
    
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.legend(title="Months", loc="upper left")
    return fig

def draw_box_plot(df: pd.DataFrame, title: str = "Year-wise Box Plot (Trend)", title2: str = "Month-wise Box Plot (Seasonality)") -> plt.Figure:
    """Draw box plots for trend and seasonality."""
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box["year"] = [d.year for d in df_box.date]
    df_box["month"] = [d.strftime('%b') for d in df_box.date]
    
    # Sort by month to ensure correct order in plot
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))
    
    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0]).set(
        xlabel="Year", 
        ylabel="Page Views",
        title=title
    )
    
    sns.boxplot(x="month", y="value", data=df_box, order=month_order, ax=axes[1]).set(
        xlabel="Month", 
        ylabel="Page Views",
        title=title2
    )
    
    return fig

def draw_interactive_line_chart(df: pd.DataFrame, aggregation_level: str):
    """Draw an interactive line chart based on aggregation level."""
    fig, ax = plt.subplots(figsize=(14, 6))
    
    if aggregation_level == "Day":
        data = df
        label = "Daily"
    elif aggregation_level == "Month":
        data = df.resample("ME").mean()
        label = "Monthly Average"
    elif aggregation_level == "Year":
        data = df.resample("YE").mean()
        label = "Yearly Average"
    else:
        st.error("Invalid aggregation level")
        return

    ax.plot(data.index, data["value"], label=label)
    ax.set_title(f"freeCodeCamp Forum Page Views ({label})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.legend()
    st.pyplot(fig)

def draw_interactive_bar_chart(df: pd.DataFrame, aggregation_level: str):
    """Draw an interactive bar chart based on aggregation level."""
    fig, ax = plt.subplots(figsize=(14, 6))
    
    if aggregation_level == "Day":
        # Too dense for a bar chart usually, but strictly following 'interactive' logic requests
        data = df.resample("D").mean() # Essentially same as df if daily
    elif aggregation_level == "Month":
        data = df.resample("ME").mean()
    elif aggregation_level == "Year":
        data = df.resample("YE").mean()
    else:
        st.error("Invalid aggregation level")
        return

    # Use simple bar plot
    ax.bar(data.index, data["value"], width=20 if aggregation_level != "Day" else 1)
    ax.set_title(f"freeCodeCamp Forum Page Views - Bar Chart ({aggregation_level})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Average Page Views")
    
    # Format x-axis for better readability if needed, but keeping it simple for now
    st.pyplot(fig)
