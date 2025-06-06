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


def seed_error_table(database_connection: pyodbc.Connection,
                     error_information: pd.Series) -> None:
    """Uploads the static error information to the database."""

    q = """
        INSERT INTO error(error_name) VALUES (?)
        """

    params = [(val,) for val in error_information.values]
    print(params)
    upload_to_database(database_connection, q, params, "error")


#############################################
# Part 2: Upload Plant and Location Tables. #
#############################################

# FOR COUNTRY

def filter_to_country_information(main_dataframe: pd.DataFrame)-> pd.DataFrame:
    """Collects a list of all relevant countries."""
    return main_dataframe['country_name'].drop_duplicates().dropna()


def seed_country_table(database_connection: pyodbc.Connection,
                       country_information: pd.DataFrame
                       ) -> None:
    """Uploads country data to the database."""

    q = """
        INSERT INTO country(country_name) VALUES (?)
        """

    params = [(val,) for val in country_information.values]

    upload_to_database(database_connection, q, params, "country")


# FOR CITY

def get_country_ids(database_connection: pyodbc.Connection) -> list[tuple]:
    """Returns a list of countries with their assigned IDs."""
    with database_connection.cursor() as cur:
        q = "SELECT country_id, country_name FROM country;"
        cur.execute(q)
        data = cur.fetchall()
    logger.debug("get_country_ids received: %s.", data)

    country_ids = {country[1]:country[0] for country in data}

    return country_ids


def filter_to_city_information(main_dataframe: pd.DataFrame,
                               country_ids: dict) -> pd.DataFrame:
    """Returns all the city information needed for the database."""

    city_data = main_dataframe[['city_name', 'country_name']].drop_duplicates().dropna()
    city_data["country_id"] = city_data["country_name"].replace(country_ids)
    logger.debug("Country ID map:\n%s", country_ids)
    logger.debug("City data:\n%s", city_data)
    return city_data


def seed_city_table(database_connection: pyodbc.Connection, 
                    city_data: pd.DataFrame) -> None:
    """Uploads city data to the database."""

    q = """
        INSERT INTO city(country_id, city_name) VALUES (?, ?)
        """
    params = list(city_data[["country_id", "city_name"]].itertuples(index=False, name=None))


    logger.debug("City data to upload:\n%s",params)
    upload_to_database(database_connection, q, params, "city")


# FOR ORIGIN

def get_city_ids(database_connection:  pyodbc.Connection) -> None:
    """Returns a list of countries with their assigned IDs."""

    with database_connection.cursor() as cur:
        q = "SELECT city_id, city_name FROM city;"
        cur.execute(q)
        data = cur.fetchall()
    logger.debug("get_city_ids received: %s.", data)

    return {city[1]: city[0] for city in data}


def filter_to_origin_information(main_dataframe: pd.DataFrame,
                                 city_ids: pd.DataFrame) -> pd.DataFrame:
    """Returns all the origin information needed for the database."""

    origin_data = main_dataframe[['origin_latitude',
                                  'origin_longitude',
                                  'city_name']].drop_duplicates().dropna()
    origin_data["city_id"] = origin_data["city_name"].replace(city_ids)
    logger.debug("City ID map:\n%s", city_ids)
    logger.debug("Origin data:\n%s", origin_data)
    return origin_data


def seed_origin_table(database_connection: pyodbc.Connection,
                      origin_data: pd.DataFrame,
                      ) -> None:
    """Uploads origin data to the database."""

    q = """
        INSERT INTO origin(city_id, origin_latitude, origin_longitude) VALUES (?, ?, ?)
        """
    params = list(origin_data[["city_id", "origin_latitude", "origin_longitude"]
                            ].itertuples(index=False, name=None))

    logger.debug("Origin data to upload:\n%s", params)
    upload_to_database(database_connection, q, params, "origin")


# FOR PLANT

def get_origin_ids(database_connection: pyodbc.Connection) -> pd.DataFrame:
    """Returns a list of all origin IDs."""

    with database_connection.cursor() as cur:
        q = "SELECT origin_id, origin_latitude, origin_longitude FROM origin;"
        cur.execute(q)
        data = cur.fetchall()
    logger.debug("get_origin_ids received: %s.", data)

    return {origin[1] + origin[2]: origin[0] for origin in data}


def filter_to_plant_information(main_dataframe: pd.DataFrame,
                                origin_ids: pd.DataFrame) -> pd.DataFrame:
    """Returns all the necessary plant information."""

    # Should include lat/long as it'll be needed.
# f"{origin[1]} {origin[2]}"
    plant_data = main_dataframe[['plant_id',
                                  'origin_latitude',
                                  'origin_longitude',
                                  'plant_name',
                                  'scientific_name'
                                  ]].drop_duplicates().dropna()
    plant_data["coords"] =   plant_data['origin_latitude'] \
                           + plant_data['origin_longitude']
    plant_data["origin_id"] = (plant_data["coords"].replace(origin_ids)).astype(int)
    logger.debug("Origin ID map:\n%s", origin_ids)
    logger.debug("Plant data:\n%s", plant_data)
    return plant_data


def seed_plant_table(database_connection: pyodbc.Connection,
                     plant_data: pd.DataFrame,
                     ) -> None:
    """
    Uploads plant data to the database, updates 
    the origin table if a plant is missing lat/long
    information.
    """


INSERT INTO plant(plant_id, origin_id, plant_name, scientific_name)
VALUES(5, 5, 'Pitcher plant', 'Sarracenia catesbaei')

(5, 5, 'Pitcher plant', 'Sarracenia catesbaei')
    q = """
        INSERT INTO plant(plant_id, origin_id, plant_name, scientific_name)
        VALUES (?, ?, ?, ?)
        """
    params = list(plant_data[["plant_id", "origin_id", "plant_name", "scientific_name"]
                              ].itertuples(index=False, name=None))

    logger.debug("Plant data to upload:\n%s", params)
    upload_to_database(database_connection, q, params, "plant")


def seed_plant_and_location_tables(connection: pyodbc.Connection,
                                   main_dataframe: pd.DataFrame,
                                     ) -> None:
    """Uploads the plant and location information to the database."""

    country_info = filter_to_country_information(main_dataframe)
    seed_country_table(connection, country_info)

    country_ids = get_country_ids(connection) # List of (country_id, country_name) tuples.
    city_info = filter_to_city_information(main_dataframe, country_ids)
    seed_city_table(connection, city_info)

    city_ids = get_city_ids(connection)
    origin_info = filter_to_origin_information(main_dataframe, city_ids)
    seed_origin_table(connection, origin_info)

    origin_ids = get_origin_ids(connection)
    plant_info = filter_to_plant_information(main_dataframe, origin_ids)
    seed_plant_table(connection, plant_info)


###################################
# Part 3: Upload Botanist Tables. #
###################################

def filter_to_botanist_information(main_dataframe: pd.DataFrame) -> pd.DataFrame:
    """Prepares data to be uploaded to the database."""
    return main_dataframe[['botanist_name', 'botanist_email', 'botanist_phone']].drop_duplicates().dropna()


def seed_botanist_table(database_connection: pyodbc.Connection,
                        botanist_information: pd.DataFrame) -> None:
    """Uploads botanist information to the database."""

    q = """
        INSERT INTO botanist(botanist_name, botanist_email, botanist_phone) VALUES (?, ?, ?)
        """
# INSERT INTO botanist(botanist_name, botanist_email, botanist_phone) VALUES ('Kenneth Buckridge', 'kenneth.buckridge@lnhm.co.uk', '763.914.8635 x57724')
    params = [(val[0], val[1], val[2]) for val in botanist_information.values]
    logger.debug("Botanist data to upload:\n%s", params)

    upload_to_database(database_connection, q, params, "botanist")


def seed_botanist_and_assignment_tables(connection: pyodbc.Connection,
                                          main_dataframe: pd.DataFrame,
                                          ) -> None:
    """
    Uploads the botanist information to the database,
    including which plants they work with.
    """
    botanist_info = filter_to_botanist_information(main_dataframe)
    seed_botanist_table(connection, botanist_info)


#####################
# General Functions #
#####################

def test_connection(connection: pyodbc.Connection) -> None:
    """Logs the connection's status."""

    with connection.cursor() as cur:
        q = "SELECT table_name, table_schema FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE';"
        cur.execute(q)
        data = cur.fetchmany()
    logger.info("Test connection received %s.", data)


def upload_to_database(connection: pyodbc.Connection,
                       query:str,
                       parameters: list[tuple],
                       table_name: str) -> None:

    with connection.cursor() as cur:
        try:
            connection.autocommit = False
            logger.info("Attempting to insert into %s table.", table_name)
            cur.executemany(query, parameters)
        except:
            connection.rollback()
            logger.warning("Rollback triggered in seed_%s_table().", table_name)
        else:
            connection.commit()
            logger.info("Committing to database in seed_%s_table().", table_name)
        finally:
            connection.autocommit = True


def seed_appropriate_tables(connection: pyodbc.Connection,
                            main_dataframe: pd.DataFrame,
                            ) -> None:
    """Calls all the seed table functions."""

    error_info = get_error_information(main_dataframe)
    logger.debug("Sensor error values: %s", error_info.values)
    seed_error_table(connection, error_info)

    seed_plant_and_location_tables(connection, main_dataframe)

    seed_botanist_and_assignment_tables(connection, main_dataframe)


########
# Main #
########

def main():
    """Makes this script easily runnable from others."""

    load_dotenv()

    all_data = main_transform()

    conn = get_database_connection()
    test_connection(conn)

    seed_appropriate_tables(conn, all_data)

    conn.close()
    logger.info("Database connection closed.")


if __name__ == "__main__":
    # main()

    load_dotenv()
    main_dataframe = main_transform()
    connection = get_database_connection()

    origin_ids = get_origin_ids(connection)
    plant_info = filter_to_plant_information(main_dataframe, origin_ids)
    seed_plant_table(connection, plant_info)
