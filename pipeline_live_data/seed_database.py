"""Transforming the extracted data."""

import ast
import logging
import json

import pandas as pd
import pyodbc

from extract import CSV_NAME
from transform import main_transform

logger = logging.getLogger(__name__)

logging.basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def create_separate_dfs(df: pd.DataFrame) -> tuple[pd.DataFrame]:
    """Returns separate dataframes based on the tables in the ERD."""

    country_df = df[['country_name']].drop_duplicates()
    city_df = df[['city_name']].drop_duplicates()
    origin_df = df[['origin_latitude', 'origin_longitude']].drop_duplicates()
    plant_df = df[['plant_id', 'plant_name',
                   'scientific_name']].drop_duplicates()
    botanist_df = df[['botanist_name', 'botanist_email',
                      'botanist_phone']].drop_duplicates()
    error_df = df[['error_name']].drop_duplicates()

    return country_df, city_df, origin_df, plant_df, botanist_df, error_df


def create_json_from_dfs(df: pd.DataFrame) -> None:
    """Creates a json from the cleaned dataframe."""

    country_df, city_df, origin_df, plant_df, botanist_df, error_df = create_separate_dfs(
        df)

    # tables = {
    #     "Country": country_df.to_dict(orient='records'),
    #     "City": city_df.to_dict(orient='records'),
    #     "Origin": origin_df.to_dict(orient='records'),
    #     "Plant": plant_df.to_dict(orient='records'),
    #     "Botanist": botanist_df.to_dict(orient='records'),
    #     "Error": error_df.to_dict(orient='records')
    # }

    tables = {
        "Country": country_df.to_json(orient='records'),
        "City": city_df.to_json(orient='records'),
        "Origin": origin_df.to_json(orient='records'),
        "Plant": plant_df.to_json(orient='records'),
        "Botanist": botanist_df.to_json(orient='records'),
        "Error": error_df.to_json(orient='records')
    }

    with open('table_seed.json', 'w', encoding='utf-8') as f:
        json.dump(tables, f, indent=4)




def get_database_connection():
    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USERNAME']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")

    connection = pyodbc.connect(conn_str)

    return connection


###############################
# Part 1: Upload Error Table. #
###############################

def upload_error_table(main_dataframe: pd.DataFrame,
                       connection:pyodbc.Connection) -> None:
    """Uploads the static error information to the database."""

    # Probably simple enough to not have sub-functions?

    pass


#############################################
# Part 2: Upload Plant and Location Tables. #
#############################################

def upload_country_table(country_data: pd.DataFrame,
                         database_connection: pyodbc.Connection) -> None:
    """Uploads country data to the database."""
    pass


def query_country_ids(database_connection:  pyodbc.Connection) -> None:
    """Returns a list of countries with their assigned IDs."""
    pass


def upload_city_table(city_data: pd.DataFrame,
                      database_connection: pyodbc.Connection) -> None:
    """
    Uploads city data to the database.
    country_data requires a list of countries with their IDs.
    """
    pass


def get_country_ids():
    """Queries the database to get a df with country & country_id."""
    pass

def upload_city_table(country_data: pd.DataFrame,
                      database_connection: pyodbc.Connection) -> None:
    """Q"""
    pass


def upload_plant_and_location_tables(main_dataframe: pd.DataFrame,
                                     connection:pyodbc.Connection) -> None:
    """Uploads the static error information to the database."""

    upload_country_table(country_dataframe, connection)

    # 
    country_ids = get_country_ids(connection)
    # Returns a df with city_name & country_id.
    city_dataframe = create_city_dataframe(main_dataframe, country_ids) 
    # Uploads city data to the database.
    upload_city_table(city_dataframe, connection)
    # This needs
    # This either needs a function that assigns each city its correct country
    # or that to be handled in the query using something like:
    # `country_id = country_id WHERE country_name = %s`
    # if it's handled in the latter way, all the queries could be written
    # then batch executed.

    # I'm not certain where the JSON comes into this?
    # Some of the code could be reused for splitting out the data?

    pass


###################################
# Part 3: Upload Botanist Tables. #
###################################

if __name__ == "__main__":

    cleaned = main_transform()
    logger.info(cleaned.info())
    logger.info(cleaned.head())
    logger.info(cleaned.columns)



    logger.info(create_json_from_dfs(cleaned))
    # logger.info(create_separate_dfs(cleaned))
