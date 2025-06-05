"""Transform script.

TEMPORARY:
Extracting gives us:
- a pandas dataframe containing plant data, extracted once an hour
- bound by anything older than (current time - 24 / 23 hours) -> 24 hours at most in rds?
    - calculated from the received_at and recording_taken columns

Assuming we have a dataframe... :
"""

from dotenv import load_dotenv

from extract import get_plant_data, get_connection


def create_csv() -> dict:
    """Creates a csv from the RDS data."""

    db_conn = get_connection()
    event_data = get_plant_data(db_conn)

    event_data['dataframe'].to_csv(event_data['file_name'], index=False)
    db_conn.close()
    return event_data


if __name__ == "__main__":

    load_dotenv()
    create_csv()
