"""Functions for creating visualisations of the archived data."""

import altair as alt
import pandas as pd
import streamlit as st


@st.cache_data
def get_temperature_over_time_chart(df: pd.DataFrame) -> alt.Chart:
    """Produces a line chart of temperature over time for each plant."""

    df['at'] = pd.to_datetime(df['at'])

    return alt.Chart(df).mark_line().encode(
        x=alt.X('at:T', title='Time'),
        y=alt.Y('temperature:Q', title='Temperature (°C)'),
        color='plant_name:N',
        tooltip=['plant_name:N', 'temperature:Q', 'at:T']
    ).properties(
        width=700,
        height=400,
        title='Plant Temperature Over Time'
    )
