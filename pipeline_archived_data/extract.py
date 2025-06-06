"""Extract script."""
# pylint: disable=I1101

from os import environ as ENV
from datetime import datetime, timedelta, timezone
import pyodbc
import pandas as pd

from dotenv import load_dotenv


def get_connection():
    """Get a connection to the database."""

    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USER']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")

    return pyodbc.connect(conn_str)


def get_file_data() -> dict:
    """Returns a dict of file specific data."""

    current_time = datetime.now(timezone.utc)
    start_window = current_time - timedelta(hours=24)
    year = start_window.strftime('%Y')

    filename = f'{start_window.strftime('%Y-%m-%d_%H-%M')}_plants.csv'

    return {
        "start_window": start_window,
        "file_name": filename,
        "bucket_key": f"{year}/{filename}"
    }


def test_select_from_db(conn: pyodbc.connect) -> list[str]:
    """Temporary test function."""

    # Testing we get a successful connection to the db.
    with conn.cursor() as cur:

        q = """SELECT table_name, table_schema FROM INFORMATION_SCHEMA.TABLES
               WHERE TABLE_TYPE='BASE TABLE';"""

        cur.execute(q)
        data = cur.fetchone()

    return list(data)


def get_plant_data(conn: pyodbc.connect) -> dict:
    """Returns all the data in the RDS older than 24 hours."""

    event_data = get_file_data()

    query = """ SELECT co.country_id, co.country_name, ci.city_id, ci.city_name, 
                o.origin_id, o.origin_latitude, o.origin_longitude,
                p.plant_id, p.plant_name, p.scientific_name,
                b.botanist_id, b.botanist_name, b.botanist_email, b.botanist_phone,
                m.measurement_id, m.temperature, m.soil_moisture, m.last_watered, m.at,
                pe.received_at, e.error_id, e.error_name
                FROM country as co
                JOIN city as ci on co.country_id = ci.country_id
                JOIN origin as o on ci.city_id = o.city_id
                JOIN plant as p on o.origin_id = p.origin_id
                JOIN plant_error as pe on p.plant_id = pe.plant_id
                JOIN error as e on pe.error_id = e.error_id
                JOIN measurement as m on p.plant_id = m.plant_id
                JOIN botanist_assignment as ba on p.plant_id = ba.plant_id
                JOIN botanist as b on ba.botanist_id = b.botanist_id
                WHERE (m.at IS NOT NULL AND m.at <= ?)
                OR (pe.received_at IS NOT NULL AND pe.received_at <= ?)
            """

    df = pd.read_sql(query, conn, params=(
        event_data['start_window'], event_data['start_window']))

    event_data['dataframe'] = df
    return event_data


if __name__ == "__main__":

    load_dotenv()

    db_conn = get_connection()

    print(get_plant_data(db_conn)['dataframe'].info())

    db_conn.close()
