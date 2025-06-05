"""Transforming the extracted data."""

import ast
import logging
import json
from os import environ as ENV

import pandas as pd
import pyodbc
from dotenv import load_dotenv

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


def get_database_connection() -> pyodbc.Connection:
    """Establish a connection with the database."""

    logger.info("Connecting to the database.")

    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USERNAME']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")

    connection = pyodbc.connect(conn_str)

    return connection


###############################
# Part 1: Upload Error Table. #
###############################

def get_error_information(main_dataframe: pd.DataFrame,):
    """Collects a list of all known errors."""
    return main_dataframe['error_name'].drop_duplicates().dropna()


def seed_error_table(error_information: pd.DataFrame,
                       connection:pyodbc.Connection) -> None:
    """Uploads the static error information to the database."""

    q = """
        INSERT INTO Error(error_name) VALUES (%s);
        """

    with connection.cursor() as cur:
        try:
            connection.autocommit = False
            cur.executemany(q, error_information.values)
        except:
            connection.rollback()
        else:
            connection.commit()
        finally:
            connection.autocommit = True


################################################
# Part 2: Upload Plant and Location Tables.    #
# Note: develop last as some questions remain. #
# TODO: Remove note!                           #
################################################

def seed_country_table(country_data: pd.DataFrame,
                         database_connection: pyodbc.Connection) -> None:
    """Uploads country data to the database."""
    pass


def query_country_ids(database_connection:  pyodbc.Connection) -> None:
    """Returns a list of countries with their assigned IDs."""
    pass


def seed_city_table(city_data: pd.DataFrame,
                      database_connection: pyodbc.Connection) -> None:
    """
    Uploads city data to the database.
    country_data requires a list of countries with their IDs.
    """
    pass


def get_country_ids() -> pd.DataFrame:
    """Queries the database to get a df with country & country_id."""
    pass


def create_city_dataframe(city_data: pd.DataFrame,
                          country_id: pd.DataFrame) -> pd.DataFrame:
    """Returns a df with city_name & country_id."""
    pass


def seed_city_table(country_data: pd.DataFrame,
                      database_connection: pyodbc.Connection) -> None:
    """Uploads city data to the database."""
    pass


def upload_plant_and_location_tables(main_dataframe: pd.DataFrame,
                                     connection:pyodbc.Connection) -> None:
    """Uploads the plant and location information to the database."""

    seed_country_table(
        main_dataframe["country_name"].drop_duplicates(),
        connection
    )

    country_ids = get_country_ids(connection)
    city_dataframe = create_city_dataframe(main_dataframe, country_ids) 
    seed_city_table(city_dataframe, connection)

    # TODO Origin (two types of query), Plant.


###################################
# Part 3: Upload Botanist Tables. #
###################################

def filter_to_botanist_information(main_dataframe: pd.DataFrame) -> pd.DataFrame:
    """Prepares data to be uploaded to the database."""
    pass


def seed_botanist_table(botanist_information: pd.DataFrame) -> None:
    """Uploads botanist information to the database."""
    pass


def upload_botanist_and_assignment_tables(main_dataframe: pd.DataFrame,
                                          connection:pyodbc.Connection) -> None:
    """
    Uploads the botanist information to the database,
    including which plants they work with.
    """
    botanist_info = filter_to_botanist_information(main_dataframe)
    seed_botanist_table(botanist_info, connection)


def seed_appropriate_tables(main_dataframe: pd.DataFrame,
                            connection: pyodbc.Connection) -> None:
    """Calls all the seed table functions."""

    conn = ...

    all_seed_data = ...

    upload_botanist_and_assignment_tables(all_seed_data, conn)


def handler():
    """What should be run when the script is properly executed."""
    
    cleaned = main_transform()
    logger.info(cleaned.info())
    logger.info(cleaned.head())
    logger.info(cleaned.columns)

    logger.info(create_json_from_dfs(cleaned))
    # logger.info(create_separate_dfs(cleaned))

def test_connection(connection: pyodbc.Connection) -> None:
    """Logs the connection's status."""

    with conn.cursor() as cur:
        q = "SELECT table_name, table_schema FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE';"
        cur.execute(q)
        data = cur.fetchmany()
    logger.info("Test connection received %s.", data)


if __name__ == "__main__":

    load_dotenv()

    all_data = main_transform()

    error_info = get_error_information(all_data)
    logger.debug("Sensor error values: %s", error_info.values)

    conn = get_database_connection()
    test_connection(conn)
    
    seed_error_table(conn, error_info)

    conn.close()
    logger.info("Database connection closed.")
