import streamlit as st
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

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
st.markdown(
    """
    <h2>Project Overview</h2>
    <p>This project aims to visualise the daily page views of the freeCodeCamp forum over a period of time, 
    from May 2016 to December 2019. The data has already been provided and will be read from a csv file. 
    The project will show information analysed in three different chart types, line chart, bar chart and box 
    and whisker chart. The line chart will show the daily page views over time, the bar chart will show the 
    average monthly page views for each year, and the box and whisker plot will show the trend of page views 
    over the years and seasonality of page views over the months.</p>
    """, unsafe_allow_html=True
)

st.markdown("---")

# information on time-series data
st.markdown(
    """
    <h2>Time-Series Data Summary</h2>
    <p>The data provided below is a time series of daily page views on freecodecamp. Each row represents a day, and 
    the first column is the date in the format yyyy-mm-ddT00:00:00 and the second column is the number of page views 
    on that date.</p>
    <p>This time series data can be used to gain insights into the website's audience and performance. 
    By analysing the page views over time, we can identify trends in the website's popularity and usage. 
    For example, we can see if there are any patterns in the page views over the course of a week, month, or year. 
    We can also see if there are any spikes or dips in the page views that correspond to specific events or promotions. 
    Additionally, we could group the data by different time periods such as weekdays, weekends or holidays to 
    understand the website's audience behaviour.</p>
    <p>Furthermore, by comparing the data to external data such as weather or other events happening in the 
    same time period, we might derive insights about how these external factors affect the website's page views.</p>
    """, unsafe_allow_html=True
)

# provide example of time-series data
st.dataframe(df.head(5), width=None)

st.markdown("---")

# information on time-series data
st.markdown(
"""
<h2>Chart Type</h2>
<p>Please use the dropdowns provided below to select the type of chart you would like to see, as well 
as see information on the benefits and limitations of using that respective chart in context of the project
with the visualisations based on Forum Page Vews.</p>
<p>You are also able to agggregate the data by day, month or year, this will adjust the interactive 
chart provided below the inital example.</p>
""", unsafe_allow_html=True)

# Add a slicer for the user to choose which chart to display
plot_type = st.selectbox("Select a chart type :", ["Line", "Bar", "Box"])

# Create a select box to choose the aggregation level (day, month, year)
aggregation_level = st.selectbox("Select the aggregation level :", ["day", "month", "year"])

st.markdown("---")

# change between diffrent types of chart

# if line chart is selected 
if plot_type == "Line":
    st.markdown("""
    <h1>Reasons for using Line Charts with Time-Series Data</h1>
    """, unsafe_allow_html=True)

    # show static line chart
    st.pyplot(draw_line_plot())

    # show line chart information
    st.markdown(
    """
    <h2>Line Plots</h2>
    <ul>
        <li>1. Line charts are a simple and effective way to visualize time-series data and identify 
        trends over time.</li>
        <li>2. They are particularly useful for showing patterns such as seasonality, long-term trends 
        and abrupt changes in the data.</li>
        <li>3. Line charts are easy to read and interpret, making them a popular choice for 
        visualizing time-series data.</li>
    </ul>
    <h3>Limitations</h3>
    <p>Line charts are not suitable for showing the distribution of the data and can be misleading if the data points are too dense.</p>
    """, unsafe_allow_html=True
    )

    # show interactive line chart title
    st.markdown("""
        <h1>Interactive Line Chart</h1>
    """, unsafe_allow_html=True)

    # show interactive line chart 
    draw_interactive_line_chart()

# if bar chart is selected
elif plot_type == "Bar":

    # show static bar chart title
    st.markdown("""
    <h1>Reasons for using Bar Charts with Time-series Data</h1>
    """, unsafe_allow_html=True)

    # show static bar chart
    (draw_bar_plot())

    # show bar chart information
    st.markdown(
    """
    <h2>Bar Charts</h2>
    <ul>
        <li>1. Bar charts are a simple and effective way to visualize time-series data and identify trends over time by comparing different categories or groups of data.</li>
        <li>2. They are particularly useful for displaying and comparing data that is categorical or discrete, such as the number of items sold in different months, or the number of students in different grade levels.</li>
        <li>3. Bar charts can be used to compare data over time, across different groups, or in different geographic regions, making them a valuable tool for data analysis and decision-making.</li>
    </ul>
    <h3>Limitations</h3>
    <p>Bar charts can be misleading when the data is not evenly spaced or when the y-axis is not starting at 0</p>
    """, unsafe_allow_html=True
    )

    # show interactive line chart title
    st.markdown("""
        <h1>Interactive Bar Chart</h1>
    """, unsafe_allow_html=True)

    # show interactive bar chart
    draw_interactive_bar_chart()
else:
    # show box chart title
    st.markdown("""
        <h1>Reasons for Using Box and Whisker Plots with Time-Series Data</h1>
    """, unsafe_allow_html=True)

    # show box chart
    st.pyplot(draw_box_plot())

    #show box chart information
    st.markdown(
    """
    <p>Box and whisker plots, also known as box plots, are a useful tool for visualizing the distribution of a dataset. They are particularly useful when working with large datasets or when you want to compare multiple sets of data at once. Box plots show the distribution of a dataset based on five key number summary: minimum, first quartile, median, third quartile, and maximum.</p>
    <p>When working with time-series data, box plots are particularly useful because they allow you to easily identify outliers and patterns in the data. For example, if you have a dataset of daily page views for a website, you can use a box plot to quickly see if there are any days that have significantly more or less page views than the others. Additionally, by grouping the data by different time periods, such as weekdays or months, you can identify patterns in the data that may not be immediately apparent.</p>
    <p>Another benefit of using box plots with time-series data is that they are not affected by the scale of the data. This means that you can easily compare datasets that have different units or ranges without having to normalize the data first. This makes box plots a useful tool for quickly identifying patterns and trends in large and complex datasets.</p>
    """, unsafe_allow_html=True
    )

st.markdown("---")