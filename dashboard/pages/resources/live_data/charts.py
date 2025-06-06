"""Functions for creating visualisations of the live data."""

import pandas as pd
import altair as alt


def pie_chart_sensor_errors() -> alt.Chart:
    """Charts the number of plants with errors or that are missing."""
    pass


def pie_chart_oob_errors() -> alt.Chart:
    """Charts the number of plants with problematic measurements."""
    pass


def line_graph_temperature(plant_data: pd.DataFrame) -> alt.Chart:
    """Charts the temperature over time for a number of plants."""
    return alt.Chart(plant_data).mark_line().encode(
        x=alt.X("at", title="Time", type="temporal"),
        y=alt.Y("temperature", title="Temperature"),
        color="plant_name"
    )


def line_graph_soil_moisture(plant_data: pd.DataFrame) -> alt.Chart:
    """Charts the soil moisture over time for a number of plants."""
    return alt.Chart(plant_data).mark_line().encode(
        x=alt.X("at", title="Time", type="temporal"),
        y=alt.Y("soil_moisture", title="Soil Moisture"),
        color="plant_name"
    )

"""
[pie chart] Number of strings errors
[pie chart] Number of OOB errors
[line graph] Temperature over time
[line graph] Soil moisture over time
"""