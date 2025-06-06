"""Functions for extracting and caching the live data."""

from os import environ as ENV

import streamlit as st
import pandas as pd
import pyodbc
from dotenv import load_dotenv


def get_mock_data(filepath: str) -> pd.DataFrame:
    """
    An example function used to load mock data.
    This doesn't need to be a function but having it
    helps show how the real data will flow.
    """
    return pd.read_csv(filepath)


def get_database_connection() -> pyodbc.Connection:
    """Establish a connection with the database."""

    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USERNAME']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")

    connection = pyodbc.connect(conn_str)

    return connection


@st.cache_resource
def get_extra_information() -> pd.DataFrame:
    """Gets all the data that was seeded into the database."""

    load_dotenv()
    conn = get_database_connection()
    with conn.cursor() as cur:
        q = """ SELECT co.country_id, co.country_name, ci.city_id, ci.city_name,
                o.origin_id, o.origin_latitude, o.origin_longitude,
                p.plant_id, p.plant_name, p.scientific_name,
                b.botanist_id, b.botanist_name, b.botanist_email, b.botanist_phone
                FROM country as co
                JOIN city as ci on co.country_id = ci.country_id
                JOIN origin as o on ci.city_id = o.city_id
                JOIN plant as p on o.origin_id = p.origin_id
                JOIN botanist_assignment as ba on p.plant_id = ba.plant_id
                JOIN botanist as b on ba.botanist_id = b.botanist_id;
            """
        cur.execute(q)
        data = cur.fetchall()

    return data


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

    return df


if __name__ == "__main__":
    # join_plant_name_to_ids()
    filename = "test_plants_extra.csv"
    mock_data = get_mock_data(filename)
    extra_information = get_extra_information()
    # Runs into issues as some plants that are on loan etc have no plant_name in the
    # available data.
    all_data = mock_data.merge(extra_information, on="plant_id")
    print(all_data)
