import streamlit as st

# create information related to project outline
def information_related_to_project_outline():
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

# information on time-series data
def time_series_data_summary():
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

# information on time-series data
def information_on_time_series_data():
        st.markdown(
    """
    <h2>Chart Type</h2>
    <p>Please use the dropdowns provided below to select the type of chart you would like to see, as well 
    as see information on the benefits and limitations of using that respective chart in context of the project
    with the visualisations based on Forum Page Vews.</p>
    <p>You are also able to agggregate the data by day, month or year, this will adjust the interactive 
    chart provided below the inital example.</p>
    """, unsafe_allow_html=True
    )

# show line chart information
def show_line_chart_information():    
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

# show bar chart information
def show_bar_chart_information():
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

#show box chart information
def show_box_chart_information():
        st.markdown(
    """
    <p>Box and whisker plots, also known as box plots, are a useful tool for visualizing the distribution of a dataset. They are particularly useful when working with large datasets or when you want to compare multiple sets of data at once. Box plots show the distribution of a dataset based on five key number summary: minimum, first quartile, median, third quartile, and maximum.</p>
    <p>When working with time-series data, box plots are particularly useful because they allow you to easily identify outliers and patterns in the data. For example, if you have a dataset of daily page views for a website, you can use a box plot to quickly see if there are any days that have significantly more or less page views than the others. Additionally, by grouping the data by different time periods, such as weekdays or months, you can identify patterns in the data that may not be immediately apparent.</p>
    <p>Another benefit of using box plots with time-series data is that they are not affected by the scale of the data. This means that you can easily compare datasets that have different units or ranges without having to normalize the data first. This makes box plots a useful tool for quickly identifying patterns and trends in large and complex datasets.</p>
    """, unsafe_allow_html=True
    )

# show interactive line chart title
def interactive_line_chart_title():
        st.markdown("""
        <h1>Interactive Line Chart</h1>
    """, unsafe_allow_html=True)
        
# show static bar chart title
def static_bar_chart_title():
        st.markdown("""
        <h1>Reasons for using Bar Charts with Time-series Data</h1>
    """, unsafe_allow_html=True)
        
# show box chart title
def box_chart_title():
        st.markdown("""
        <h1>Reasons for Using Box and Whisker Plots with Time-Series Data</h1>
    """, unsafe_allow_html=True)
        
# show interactive line chart title
def interactive_bar_chart_title():
        st.markdown("""
        <h1>Interactive Bar Chart</h1>
    """, unsafe_allow_html=True)
        
    #show box chart information
def box_chart_information():
        st.markdown(
    """
    <p>Box and whisker plots, also known as box plots, are a useful tool for visualizing the distribution of a dataset. They are particularly useful when working with large datasets or when you want to compare multiple sets of data at once. Box plots show the distribution of a dataset based on five key number summary: minimum, first quartile, median, third quartile, and maximum.</p>
    <p>When working with time-series data, box plots are particularly useful because they allow you to easily identify outliers and patterns in the data. For example, if you have a dataset of daily page views for a website, you can use a box plot to quickly see if there are any days that have significantly more or less page views than the others. Additionally, by grouping the data by different time periods, such as weekdays or months, you can identify patterns in the data that may not be immediately apparent.</p>
    <p>Another benefit of using box plots with time-series data is that they are not affected by the scale of the data. This means that you can easily compare datasets that have different units or ranges without having to normalize the data first. This makes box plots a useful tool for quickly identifying patterns and trends in large and complex datasets.</p>
    """, unsafe_allow_html=True
    )

# line chart time-series title
def line_chart_time_series_title():
        st.markdown("""
    <h1>Reasons for using Line Charts with Time-Series Data</h1>
    """, unsafe_allow_html=True)