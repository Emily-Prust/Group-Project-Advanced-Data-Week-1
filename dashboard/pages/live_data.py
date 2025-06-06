"""The dashboard page for real-time sensor data."""

import pandas as pd
import streamlit as st

from resources.live_data.charts import (line_graph_temperature, line_graph_soil_moisture,
                                        pie_chart_oob_errors)
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


def create_oob_information(measurement_data: pd.DataFrame) -> pd.DataFrame:
    """Creates out of bounds information to plot in a pie chart."""
    temp_lower_bound = 10
    temp_upper_bound = 30
    moisture_lower_bound = 20
    moisture_upper_bound = 100

    no_issue_count = measurement_data[
        ((measurement_data["temperature"] > temp_lower_bound) &
         (measurement_data["temperature"] < temp_upper_bound))
        & ((measurement_data["soil_moisture"] > moisture_lower_bound) &
           (measurement_data["soil_moisture"] < moisture_upper_bound))].shape[0]

    temperature_issue_count = measurement_data[
        ~ ((measurement_data["temperature"] > temp_lower_bound) &
           (measurement_data["temperature"] < temp_upper_bound))
        & ((measurement_data["soil_moisture"] > moisture_lower_bound) &
           (measurement_data["soil_moisture"] < moisture_upper_bound))].shape[0]

    soil_moisture_issue_count = measurement_data[
        ((measurement_data["temperature"] > temp_lower_bound) &
         (measurement_data["temperature"] < temp_upper_bound))
        & ~ ((measurement_data["soil_moisture"] > moisture_lower_bound) &
             (measurement_data["soil_moisture"] < moisture_upper_bound))].shape[0]

    multiple_issues_count = measurement_data[
        ~ ((measurement_data["temperature"] > temp_lower_bound) &
           (measurement_data["temperature"] < temp_upper_bound))
        & ~ ((measurement_data["soil_moisture"] > moisture_lower_bound) &
             (measurement_data["soil_moisture"] < moisture_upper_bound))].shape[0]

    return pd.DataFrame({"oob_status": ["No Issue",
                                                   "Temperature Issue",
                                                   "Soil-Moisture Issue",
                                                   "Multiple Issues"],
                                    "count": [no_issue_count,
                                              temperature_issue_count,
                                              soil_moisture_issue_count,
                                              multiple_issues_count]})


def main_display(measurement_data: pd.DataFrame):
    """Elements displayed at the top of the page."""

    st.dataframe(measurement_data[["plant_name",
                                    "temperature",
                                     "soil_moisture",
                                    "last_watered"]],
                  height=180)

    right_subcolumn, left_subcolumn = st.columns([1, 1])

    with right_subcolumn:
        st.altair_chart(line_graph_temperature(measurement_data))

    with left_subcolumn:
        st.altair_chart(line_graph_soil_moisture(measurement_data))


def main():

    st.set_page_config(layout="wide",
                       initial_sidebar_state="collapsed")

    filename = "resources/live_data/test_plants_extra.csv"
    data = get_mock_data(filename)

    st.title("LMNH Botanical Live Dashboard")
    left_column, right_column = st.columns([1, 3])


    with left_column:
        data = user_filtering(data)
        measurement_data = data[["plant_id", "plant_name", "temperature", "soil_moisture",
                                 "last_watered", "at", ]].dropna()
        error_data = data[["plant_id", "error_name"]]
        
        oob_information = create_oob_information(measurement_data)

        st.altair_chart(pie_chart_oob_errors(oob_information))

    with right_column:
        main_display(measurement_data)


if __name__ == "__main__":
    main()