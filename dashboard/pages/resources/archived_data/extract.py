"""Functions for extracting and caching the archived data."""
import pandas as pd
import streamlit as st


@st.cache_data
def load_data(file_name: str) -> pd.DataFrame:
    """Loading the data to a dataframe.
    Currently reads from a csv, can be changed to loading from RDS in future.
    """
    return pd.read_csv(file_name)


@st.cache_resource
def filter_plants(df: pd.DataFrame, plant_names: list[str]) -> pd.DataFrame:
    """Filter plant data by specific plant names."""
    return df[df["plant_name"].isin(plant_names)]
