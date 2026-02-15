"""Text content and documentation for the Intelligence Flux dashboard.

This module provides explanatory text and guides displayed in the
Streamlit dashboard, separated from presentation logic.
"""

import streamlit as st

# Content strings separated from presentation
HEADER_GUIDE_CONTENT = """
### The Intelligence Flux Framework

Welcome to the **V3 Intelligence Flux** platform. This engine is designed
to transform complex web traffic into strategic clarity.

**Guiding Principles:**

1. **Signal over Noise**: We prioritise trends (Impression Flux) over daily volatility.
2. **Context over Raw Data**: Every chart includes a "Strategy Tip" to help you act
   on the information.
3. **Global Symmetry**: The dashboard is interactive—filters in the sidebar propagate
   through every specialised tab.
"""

OVERVIEW_CONTENT = """
### Impression Flux & Quality Pulse

This module monitors the fundamental volume and health of your platform.

#### Impression Flux (Volume Analysis)

This chart tracks the aggregate "pulse" of your audience.

- **How to read**: Look for the gradient of the line. A steady upward slope
  indicates healthy organic growth, while horizontal lines suggest saturation.
- **Strategy Tip**: If you see a "plateau," it's time to investigate new
  acquisition channels or geography segments in the sidebar.

#### Cyclical Variance (Seasonality)

Web traffic is rarely linear. This chart groups data by month to reveal
the "Standard Seasonality."

- **How to read**: Compare bars month-over-month. For most platforms,
  you'll see a 'V' shape (dip in summer, spike in winter).
- **Strategy Tip**: Use this to plan marketing spend. Boost your budget
  during the natural 'peak' months to ride the momentum.
"""

AUDIENCE_CONTENT = """
### Global Reach & Access Modality

Understanding the "Who" and "Where" behind the impressions.

#### Global Reach Index (The Map)

Our high-fidelity choropleth map reveals your population nodes.

- **Intensity**: Darker shades represent your primary markets. Hover over
  a country to see exact impression volume.
- **Interactivity**: You can zoom and pan. Use the sidebar to isolate a
  single region (e.g., North America) to see granular country variance.

#### Source Concentration (Top Locales)

Reveals the "Head" vs "Long Tail" of your traffic.

- **Strategic Use**: If the top 3 countries account for >70% of traffic,
  your risk is high. Diversifying this distribution is a key growth lever.

#### Interface Matrix (Device Strategy)

Access is behaviour.

- **Desktop**: Indicates high intent, long-form consumption, or professional usage.
- **Mobile/Tablet**: Indicates casual, rapid-fire, or social discovery consumption.
- **Strategy Tip**: If your "Bounce Index" is higher on Mobile than Desktop,
  your mobile experience likely needs optimisation.
"""

PERFORMANCE_CONTENT = """
### User Behaviour Dynamics (Quality Index)

The most critical view for understanding if your content is actually resonating.

- **Duration (Rose)**: How many seconds, on average, a visitor stays.
  Growth here is the ultimate indicator of "Stickiness."
- **Bounce (Sky)**: The probability that a user leaves after one page.
  High bounce + low duration = "Search Mismatch" (they didn't find what
  they expected).

**The Golden Correlation:**

When **Duration** goes up and **Bounce** goes down simultaneously, you have
achieved **High-Loyalty Flux**. This is the state where every impression is
contributing to long-term community value.
"""

ANOMALY_CONTENT = """
### Signal Intelligence & Variation

Advanced modelling to ensure you aren't fooled by random noise.

#### Signal Intelligence

We flag outliers that deviate by more than 3 standard deviations from the norm.

- **High Spike**: Viral success or marketing impact.
- **Low Dip**: Technical failure or regional outage.

#### Evolutionary Variance (Distribution)

Shows the statistical "Spread" of your traffic by Year and Month.

- **The Box**: Represents the middle 50% of your data (The Interquartile Range).
- **The Median Line**: The true centre of your traffic volume.
- **How to use**: If the "Box" is shifting upward over the years, your platform
  is evolving and maturing. If the boxes are getting "shorter," your traffic
  is becoming more predictable and stable.
"""


def header_guide() -> None:
    """Display a high-level guide for the Intelligence Flux platform.

    Renders the framework introduction and guiding principles in
    the Streamlit sidebar expander.

    Example:
        >>> with st.expander("Quick Start Guide"):
        ...     header_guide()
    """
    st.markdown(HEADER_GUIDE_CONTENT)


def project_overview() -> None:
    """Display detailed overview of the Performance tab.

    Renders explanations for Impression Flux and Cyclical Variance
    charts with strategic interpretation guidance.

    Example:
        >>> with tab_performance:
        ...     project_overview()
        ...     st.plotly_chart(draw_line_plot(df))
    """
    st.markdown(OVERVIEW_CONTENT)


def audience_info() -> None:
    """Display explanation of audience and geographic metrics.

    Renders guidance for interpreting the Global Reach map,
    Source Concentration bar chart, and Interface Matrix donut chart.

    Example:
        >>> with tab_audience:
        ...     audience_info()
        ...     st.plotly_chart(draw_regional_map(df))
    """
    st.markdown(AUDIENCE_CONTENT)


def performance_info() -> None:
    """Display explanation of behaviour and engagement metrics.

    Renders interpretation guidance for the User Flux Dynamics
    dual-axis chart showing session duration and bounce rate.

    Example:
        >>> with tab_engagement:
        ...     performance_info()
        ...     st.plotly_chart(draw_engagement_metrics(df))
    """
    st.markdown(PERFORMANCE_CONTENT)


def anomaly_info() -> None:
    """Display explanation of anomaly detection and statistical outliers.

    Renders guidance for interpreting Signal Intelligence markers
    and Evolutionary Variance box plots.

    Example:
        >>> with tab_intelligence:
        ...     anomaly_info()
        ...     st.plotly_chart(draw_anomaly_highlight(df, anomalies))
    """
    st.markdown(ANOMALY_CONTENT)
