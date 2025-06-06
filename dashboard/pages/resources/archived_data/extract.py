"""Functions for extracting and caching the archived data."""
import logging
import pandas as pd
import streamlit as st

logger = logging.getLogger(__name__)

logging.basicConfig(
    level="WARNING",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


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


@st.cache_resource
def get_plant_id_to_name_mapping(df: pd.DataFrame) -> dict[int, str]:
    """Get a mapping of plant_id to plant_name."""
    mapping_df = df.dropna(subset=['plant_id', 'plant_name'])
    return dict(mapping_df[['plant_id', 'plant_name']].drop_duplicates().values)


@st.cache_resource
def map_plant_id_to_name(df: pd.DataFrame) -> pd.DataFrame:
    plant_id_to_name = get_plant_id_to_name_mapping(df)
    df['plant_name'] = df.apply(
        lambda row: plant_id_to_name.get(row['plant_id'], row['plant_name']),
        axis=1
    )

    missing_names = df[df['plant_name'].isna() & df['plant_id'].notna()]
    unmatched_ids = set(missing_names['plant_id']) - \
        set(plant_id_to_name.keys())
    logger.warning(f"Unmatched plant IDs: {unmatched_ids}")

    return df


@st.cache_resource
def flag_errors(df: pd.DataFrame) -> pd.DataFrame:
    """Sets error_name to 'invalid temp' or 'low moisture' if abnormal readings."""
    temp_condition = (df['temperature'] < 10) | (df['temperature'] > 30)
    df.loc[temp_condition & df['error_name'].isna(), 'error_name'] = 'invalid temp'

    moisture_cond = df['soil_moisture'] < 20
    df.loc[moisture_cond & df['error_name'].isna(), 'error_name'] = 'low_moisture'
    return df
