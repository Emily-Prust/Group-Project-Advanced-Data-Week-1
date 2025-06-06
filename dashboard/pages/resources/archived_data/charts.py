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
        tooltip=['plant_name:N', 'temperature:Q', 'at:T']
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
        tooltip=['plant_name:N', 'soil_moisture:Q', 'at:T']
    ).properties(
        width=600,
        height=400
    )
