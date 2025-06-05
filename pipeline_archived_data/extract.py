"""Extract script."""
# pylint: disable=I1101

from os import environ as ENV
import pyodbc
import pandas as pd

from dotenv import load_dotenv


def get_connection():
    """Get a connection to the database."""

    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USER']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")

    return pyodbc.connect(conn_str)


def get_plant_data(conn: pyodbc.connect) -> pd.DataFrame:
    """Returns all the data in the RDS older than 24 hours."""

    # Testing we get a successful connection to the db.
    with conn.cursor() as cur:
        q = """SELECT table_name, table_schema FROM INFORMATION_SCHEMA.TABLES
               WHERE TABLE_TYPE='BASE TABLE';"""
        cur.execute(q)
        data = cur.fetchone()

    conn.close()
    return list(data)


if __name__ == "__main__":

    load_dotenv()
    print(get_plant_data(get_connection()))
