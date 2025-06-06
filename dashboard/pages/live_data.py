"""The dashboard page for real-time sensor data."""

import numpy as np
import pandas as pd
import streamlit as st

from resources.live_data.charts import line_graph_temperature, line_graph_soil_moisture
from resources.live_data.extract import get_mock_data


def user_filtering(data_to_filter: pd.DataFrame):
    """Allows the user to filter by either botanist or plant."""

    is_filtered_by_botanist = st.toggle("Filter by botanist?")

    if is_filtered_by_botanist:
        selected_botanists = st.multiselect(label="Botanists",
                                            options=data_to_filter[
                                                "botanist_name"].dropna().unique())
        data = data_to_filter[data_to_filter["botanist_name"].isin(
            selected_botanists)]

    else:
        selected_plants = st.multiselect(label="Plants",
                                         options=data_to_filter[
                                             "plant_name"].dropna().unique())
        data = data_to_filter[data_to_filter["plant_name"].isin(
            selected_plants)]

    return data


if __name__ == "__main__":

    st.set_page_config(layout="wide",
                       initial_sidebar_state="collapsed")

    st.title("LMNH Botanical Live Dashboard")

    filename = "resources/live_data/test_plants_extra.csv"
    data = get_mock_data(filename)

    left_column, right_column = st.columns([1, 3])

    with left_column:
        data = user_filtering(data)
        measurement_data = data[["plant_id", "plant_name", "temperature", "soil_moisture",
                                 "last_watered", "at", ]].dropna()
        error_data = data[["plant_id", "error_name"]]
        # Pie chart for high-level errors.
        # Pie chart for measurements.

    with right_column:

        st.dataframe(measurement_data[["plant_name", 
                                       "temperature", 
                                       "soil_moisture",
                                       "last_watered"]],
                    height=180)
        st.dataframe(error_data,
                     height=180)
        right_subcolumn, left_subcolumn = st.columns([1,1])
        with right_subcolumn:
            st.altair_chart(line_graph_temperature(measurement_data))
        with left_subcolumn:
            st.altair_chart(line_graph_soil_moisture(measurement_data))


    _comment = """
    Necessary pieces:
    [input] Botanist selection
        In: list of botanist names.
        Out: Botanist selection widget
        [filter the data based on selected botanist]

    [pie chart] Number of string errors
    [pie chart] Number of OOB errors
    [table] Live plant data
    [table] Live error data
    [line graph] Temperature over time
    [line graph] Soil moisture over time

    """
