"""The dashboard page for long-term sensor data."""
import logging

import streamlit as st
import pandas as pd

from resources.archived_data.extract import (
    load_data, filter_plants, map_plant_id_to_name, flag_errors)
from resources.archived_data.charts import (
    get_temperature_over_time_chart, get_soil_moisture_over_time_chart)


logger = logging.getLogger(__name__)

logging.basicConfig(
    level="WARNING",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def display_temperature_chart(df: pd.DataFrame):
    """Display the temperature over time chart."""
    st.subheader('Plant Temperature Over Time')
    st.altair_chart(get_temperature_over_time_chart(df))


def display_soil_moisture_chart(df: pd.DataFrame):
    """Display the soil moisture over time chart."""
    st.subheader('Plant Soil Moisture Over Time')
    st.altair_chart(get_soil_moisture_over_time_chart(df))


def get_sidebar_plant_measurement_filter(df: pd.DataFrame) -> list[str]:
    """Make the plant filter in the sidebar, and return only relevant plants names."""
    with st.sidebar:
        st.header("Plant Filter")
        df = df.dropna(subset=['plant_name'])
        selected_plants = st.multiselect(
            "Select Plants", df['plant_name'].unique())

    return selected_plants


def display_measurement_data(df: pd.DataFrame):
    """Displays the temperature and soil moisture charts."""
    df['at'] = pd.to_datetime(df['at'], format='mixed')

    selected_plants = get_sidebar_plant_measurement_filter(df)

    filtered_plants = filter_plants(df, selected_plants)

    left, right = st.columns(2)
    with left:
        display_temperature_chart(filtered_plants)

    with right:
        display_soil_moisture_chart(filtered_plants)


def get_sidebar_plant_error_filter(df: pd.DataFrame) -> str:
    """Make the plant filter in the sidebar, and return only the selected plant name."""
    with st.sidebar:
        st.header("Plant Filter")
        df = df.dropna(subset=['plant_name'])
        selected_plant = st.selectbox(
            "Select Plant", df['plant_name'].unique())

    return selected_plant


def display_average_temp(df: pd.DataFrame):
    """Displays the average temp for a selected plant."""
    avg_temp = df['temperature'].mean()
    st.metric(label="Average Temperature (°C)", value=f"{avg_temp:.2f}")


def display_average_moisture(df: pd.DataFrame):
    """Displays the average soil moisture for a selected plant."""
    avg_moisture = df['soil_moisture'].mean()
    st.metric(label="Average Soil Moisture (%)", value=f"{avg_moisture:.2f}")


def display_extra_plant_info(df: pd.DataFrame):
    """Displays additional plant info in a box."""
    with st.container():
        st.markdown("#### Additional Information")

        measurement_error = df['error_name'].isin(
            ['invalid_temp', 'low_moisture']).sum()
        sensor_errors = len(df[df['error_name'].notna()]) - measurement_error
        total_readings = len(df)
        assigned_botanists = df['botanist_name'].dropna().unique()

        st.markdown(f"- **Number of Measurement Errors:** {measurement_error}")
        st.markdown(f"- **Number of Sensor Errors:** {sensor_errors}")
        st.markdown(f"- **Total Readings:** {total_readings}")
        st.markdown("#### **Assigned Botanists:**")
        for botanist in assigned_botanists:
            st.markdown(f"  - {botanist}")


def display_error_data(df: pd.DataFrame):
    """Displays the error data for one plant."""

    df = map_plant_id_to_name(df)
    df = flag_errors(df)

    selected_plant = get_sidebar_plant_error_filter(df)

    single_plant = filter_plants(df, [selected_plant])

    st.subheader(f"Information for {selected_plant}.")

    left, right = st.columns(2)
    with left:
        display_average_temp(single_plant)

    with right:
        display_average_moisture(single_plant)
        display_extra_plant_info(single_plant)


if __name__ == "__main__":
    df = load_data("test_plants_extra.csv")

    # remove this and put into homepage.py i think
    st.set_page_config(layout="wide",
                       initial_sidebar_state="collapsed")

    st.title("Historical Data")

    display_measurement_data(df)
    display_error_data(df)

    logger.debug(df.head())
    logger.debug(df.columns)
    logger.debug(df.dtypes)
    logger.debug(df['at'])
