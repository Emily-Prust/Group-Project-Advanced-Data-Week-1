"""Functions for creating visualisations of the archived data."""

import altair as alt
import pandas as pd
import streamlit as st


@st.cache_data
def get_temperature_over_time_chart(df: pd.DataFrame) -> alt.Chart:
    """Produces a line chart of temperature over time for each plant."""

    return alt.Chart(df).mark_line().encode(
        x=alt.X('at:T', title='Time'),
        y=alt.Y('temperature:Q', title='Temperature (°C)'),
        color=alt.Color('plant_name:N', title='Plant'),
        tooltip=['plant_name', 'temperature', 'at']
    ).properties(
        width=600,
        height=400
    )


@st.cache_data
def get_soil_moisture_over_time_chart(df: pd.DataFrame) -> alt.Chart:
    """Produces a line chart of soil moisture over time for each plant."""

    return alt.Chart(df).mark_line().encode(
        x=alt.X('at:T', title='Time'),
        y=alt.Y('soil_moisture:Q', title='Soil Moisture (%)'),
        color=alt.Color('plant_name:N', title='Plant'),
        tooltip=['plant_name', 'soil_moisture', 'at']
    ).properties(
        width=600,
        height=400
    )


@st.cache_data
def get_error_distribution_chart(df: pd.DataFrame) -> alt.Chart:
    """Produces a donut chart of error distributions."""
    measurement_error = df['error_name'].isin(
        ['invalid_temp', 'low_moisture']).sum()
    sensor_errors = len(df[df['error_name'].notna()]) - measurement_error
    no_error = len(df) - measurement_error - sensor_errors

    error_counts = pd.DataFrame({
        'error_category': ['No Error', 'Sensor Error', 'Measurement Error'],
        'count': [no_error, sensor_errors, measurement_error]
    })

    return alt.Chart(error_counts).mark_arc(innerRadius=50).encode(
        theta="count:Q",
        color=alt.Color("error_category:N", title="Error Category"),
        tooltip=["error_category", "count"]
    ).properties(
        width=600,
        height=600
    )
