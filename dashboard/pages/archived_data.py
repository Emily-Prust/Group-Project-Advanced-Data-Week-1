"""The dashboard page for long-term sensor data."""
import logging

import streamlit as st
import pandas as pd

from resources.archived_data.extract import load_data, filter_plants
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


def get_sidebar_plant_filter(df: pd.DataFrame) -> pd.DataFrame:
    """Make the plant filter in the sidebar, and return only relevant plants."""
    with st.sidebar:
        st.header("Plant Filter")
        df = df.dropna(subset=['plant_name'])
        selected_plants = st.multiselect(
            "Select Plants", df['plant_name'].unique())

    return selected_plants


def display_measurement_data(df: pd.DataFrame):
    """Displays the temperature and soil moisture charts."""

    selected_plants = get_sidebar_plant_filter(df)

    filtered_plants = filter_plants(df, selected_plants)

    left, right = st.columns(2)
    with left:
        display_temperature_chart(filtered_plants)

    with right:
        display_soil_moisture_chart(filtered_plants)


if __name__ == "__main__":
    df = load_data("test_plants_historical.csv")

    # remove this and put into homepage.py i think
    st.set_page_config(layout="wide")

    st.title("Historical Data")

    display_measurement_data(df)

    logger.debug(df.head())
    logger.debug(df.columns)
    logger.debug(df.dtypes)
    logger.debug(df['at'])
