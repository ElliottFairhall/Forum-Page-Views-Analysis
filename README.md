# freecodecamp-data-analysis

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://elliottfairhall-forum-page-views-analysis-main-3fr0fy.streamlit.app/)

## Project Overview

This project is a simple data analysis application built using the Python programming language and the Streamlit framework. The purpose of this application is to visualize the daily page views of the freecodeCamp forum from 2016 to 2019. The application provides users with the ability to select the level of aggregation of the data, whether daily, monthly, or yearly. The user can also view the data as a line plot or a bar chart.


## Requirements

### Software Requirements

-   Python 3.6 or higher
-   Streamlit
-   Pandas
-   Seaborn
-   Matplotlib
-   PIL

### Hardware Requirements

No specific hardware requirements are needed to run this code.

## Installation Instructions

1.  Install Python 3.x from the official website.
2.  Install Streamlit, Pandas, Seaborn, Matplotlib, and PIL using pip package manager by running the following command in the terminal or command prompt:

Copy code

`pip install streamlit pandas seaborn matplotlib pillow` 

## Running Instructions

1.  Save the code shared above to a file with a `.py` extension (e.g., `filename.py`).
2.  Open the command prompt or terminal in the directory where the file is saved.
3.  Run the following command to start the Streamlit application:

Copy code

`streamlit run filename.py` 

4.  Open a web browser and navigate to the URL shown in the terminal or command prompt after running the above command.

## Input Requirements

The code reads data from a CSV file named `fcc-forum-pageviews.csv` which should be placed in the `assets/data/` directory relative to the file containing the code. The data in this file should have the following columns:

-   `date` (string): The date in the format 'YYYY-MM-DD'
-   `value` (integer): The number of pageviews for that day

## Output

The code generates two plots: a line plot and a bar plot. Both plots display the daily freecodeCamp forum page views for a given time period. The line plot is drawn using the `draw_line_plot()` function, while the bar plot is drawn using the `draw_bar_plot()` function. Both functions take the following parameters:

-   `df`: a pandas dataframe containing the data to be plotted
-   `title`: a string representing the title of the plot
-   `xlabel`: a string representing the x-axis label of the plot
-   `ylabel`: a string representing the y-axis label of the plot

The code also generates an interactive line chart and an interactive bar chart using the `draw_interactive_line_chart()` and `draw_interactive_bar_chart()` functions, respectively. The interactive charts allow the user to select the aggregation level (day, month, or year) and display the corresponding chart. If an invalid aggregation level is selected, a warning message is displayed.

Note: The charts are interactive, and they are displayed in the web browser when the Streamlit application is running.
## Business Case

The application can be useful for analyzing the traffic of the freecodeCamp forum from 2016 to 2019. The line plot can be used to identify trends in the daily page views of the forum, while the bar chart can be used to identify the months with the highest and lowest average page views. This information can be used to make data-driven decisions for marketing and advertising efforts on the forum. For example, if certain months consistently have higher page views, the forum could choose to allocate more advertising resources during those times to capitalize on the increased traffic. Conversely, if certain months consistently have lower page views, the forum could choose to focus on improving content and engagement during those times to boost traffic.
