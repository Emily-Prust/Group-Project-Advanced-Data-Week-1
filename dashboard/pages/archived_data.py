"""The dashboard page for long-term sensor data."""
import logging

import streamlit as st
import pandas as pd

from resources.archived_data.extract import load_data, filter_plants
from resources.archived_data.charts import get_temperature_over_time_chart

logger = logging.getLogger(__name__)

logging.basicConfig(
    level="DEBUG",  # Change to WARNING
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def display_temperature_chart(df: pd.DataFrame):
    """Display the temperature over time chart."""
    st.subheader("Temperature over time.")

    df = df.dropna(subset=['plant_name'])
    relevant_plants = st.multiselect(
        "Select Plants", df['plant_name'].unique())

    filtered_plants = filter_plants(df, relevant_plants)

    st.altair_chart(get_temperature_over_time_chart(filtered_plants))


if __name__ == "__main__":
    df = load_data("test_plants_historical.csv")

    # remove this and put into homepage.py i think
    st.set_page_config(layout="wide")

    st.title("Historical Data")

    display_temperature_chart(df)

    # logger.debug(df.head())
    # logger.debug(df.columns)
    # logger.debug(df.dtypes)
    # logger.debug(df['at'])
