import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns

from pandas.plotting import register_matplotlib_converters
from pathlib import Path
from PIL import Image
from Text_Functions import information_related_to_project_outline, time_series_data_summary, information_on_time_series_data, show_line_chart_information, interactive_line_chart_title, static_bar_chart_title, show_bar_chart_information, box_chart_title, interactive_bar_chart_title, box_chart_information, line_chart_time_series_title

PAGE_ICON = ":chart_with_upwards_trend:"

PAGE_TITLE = "Data Engineer, Educator Analyst and Technology Enthusiast"

# Set the title and icon of the application
st.set_page_config(page_title = PAGE_TITLE, page_icon = PAGE_ICON, layout="centered")

# Set the path for the home page, csv file and css file
current_dir = Path(__file__).parent if "_file_" in locals() else Path.cwd()
home_page = current_dir / "Home_Page.py"
Website_image = current_dir / "assets"/ "images" / "Website.jpg"
csv_file = current_dir / "assets" / "data" / "fcc-forum-pageviews.csv"
css_file = current_dir / "styles" / "main.css"

# Read the css file and add it to the streamlit application
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

# Read the csv file and set the date column as the index
df = pd.read_csv(csv_file, parse_dates=["date"], index_col=["date"])

# Remove any outliers from the data by only keeping values within the 2.5 and 97.5 percentiles
df = df[(df["value"] >= df["value"].quantile(0.025)) & (df["value"] <= df["value"].quantile(0.975))]

# Data preparation function
def prepare_data(df):
    # Validate the dataframe
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Data must be a DataFrame")
    if 'date' not in df.columns:
        raise ValueError("Dataframe must have a 'date' column")
    if 'value' not in df.columns:
        raise ValueError("Dataframe must have a 'value' column")

    # Parse the date column
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)
    return df

# Function to draw the line plot
def draw_line_plot(df=df, title="Line Plot", xlabel="X-axis", ylabel="Y-axis"):
    if df is None:
        raise ValueError("Dataframe is missing")
    fig, ax = plt.subplots()
    ax.plot(df.index, df["value"], 'r', linewidth=1)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return fig

# Function to draw interactive line chart
def draw_interactive_line_chart():

    if aggregation_level == "day":
        # Plot the daily page views
        df.plot(kind='line', xlabel='date', ylabel='Page Views')
    elif aggregation_level == "month":
        # Group the data by month and plot the mean page views
        df_month = df.resample('M').mean()
        df_month.plot(kind='line', xlabel='date', ylabel='Page Views')
    elif aggregation_level == "year":
        # Group the data by year and plot the mean page views
        df_year = df.resample('Y').mean()
        df_year.plot(kind='line', xlabel='date', ylabel='Page Views')
        # provide warning if aggregation level not selected
    else:
        st.warning("Invalid aggregation level selected")
    plt.title("Daily freecodeCamp Forum Page Views")
    st.pyplot(plt.gcf())

# Function to draw the bar chart
def draw_bar_plot(df=df, title="Bar Plot", xlabel="X-axis", ylabel="Y-axis"):
    if df is None:
        raise ValueError("Dataframe is missing")
    df["month"] = df.index.month
    df["year"] = df.index.year
    df_bar = df.groupby(["year", "month"])["value"].mean()
    df_bar = df_bar.unstack()
    ax = df_bar.plot(kind='bar', stacked=True)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=0)
    plt.legend(["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    for i in ax.containers:
        for j in i:
            ax.text(j.get_x() + j.get_width()/2., j.get_y() + j.get_height()/2.,
                    '%d' % int(j.get_height()), ha='center', va='center', fontsize=6)
    return plt

# Function to draw interactive bar chart
def draw_interactive_bar_chart():

    if aggregation_level == "day":
        # Plot the daily page views
        df.plot(kind='bar', xlabel='date', ylabel='Page Views')
    elif aggregation_level == "month":
        # Group the data by month and plot the mean page views
        df_month = df.resample('M').mean()
        df_month.plot(kind='bar', xlabel='date', ylabel='Page Views')
    elif aggregation_level == "year":
        # Group the data by year and plot the mean page views
        df_year = df.resample('Y').mean()
        df_year.plot(kind='bar', xlabel='date', ylabel='Page Views')
        # provide warning if aggregation level not selected
    else:
        st.warning("Invalid aggregation level selected")
    plt.title("Daily freecodeCamp Forum Page Views")
    st.pyplot(plt.gcf())

# Function to draw box and whisker plot
def draw_box_plot(df=df, title="Box and Whisker Plot", xlabel="X-axis", ylabel="Y-axis"):
    if df is None:
        raise ValueError("Dataframe is missing")
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box['date']]
    df_box['month'] = [d.strftime('%b') for d in df_box['date']]

    # Add a month_num column to the dataframe and sort it by this column
    df_box["month_num"] = df_box["date"].dt.month
    df_box = df_box.sort_values("month_num")

    # Create subplots for year-wise and month-wise box plots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10,5))
    axes[0]=sns.boxplot(x=df_box["value"], y=df_box["year"], ax = axes[0])
    axes[1]=sns.boxplot(x=df_box["value"], y=df_box["month"], ax = axes[1])

    # Set the titles and labels for the subplots
    axes[0].set_title(f"{title} (Trend)")
    axes[0].set_xlabel(xlabel)
    axes[0].set_ylabel("Year")
    axes[1].set_title(f"{title} (Seasonality)")

# provide title for page
st.markdown("<h1>Time-Series Analysis of FreeCodeCamp Forum Page Views</h1>",  unsafe_allow_html=True)

st.markdown("---")

#open website_image for page
image = Image.open(Website_image)
st.image(image)

# create information related to project outline
information_related_to_project_outline()

st.markdown("---")

# information on time-series data
information_on_time_series_data()

# provide example of time-series data
st.dataframe(df.head(5), width=None)

st.markdown("---")

# information on time-series data
information_on_time_series_data()

# Add a slicer for the user to choose which chart to display
plot_type = st.selectbox("Select a chart type :", ["Line", "Bar", "Box"])

# Create a select box to choose the aggregation level (day, month, year)
aggregation_level = st.selectbox("Select the aggregation level :", ["day", "month", "year"])

st.markdown("---")

# change between diffrent types of chart

# if line chart is selected 
if plot_type == "Line":

# line chart time-series title
    line_chart_time_series_title()

    # show static line chart
    st.pyplot(draw_line_plot())

    # show line chart information
    show_line_chart_information()
    
    # show interactive line chart title
    interactive_line_chart_title()

    # show interactive line chart 
    draw_interactive_line_chart()

# if bar chart is selected
elif plot_type == "Bar":

    # show static bar chart title
    static_bar_chart_title()

    # show static bar chart
    (draw_bar_plot())

    # show bar chart information
    show_bar_chart_information()

    # show interactive bar chart title
    interactive_bar_chart_title()

    # show interactive bar chart
    draw_interactive_bar_chart()
else:
    # show box chart title
    box_chart_title()

    # show box chart
    st.pyplot(draw_box_plot())

    #show box chart information
    box_chart_information()

st.markdown("---")