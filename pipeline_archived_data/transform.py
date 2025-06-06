"""Transform script."""

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
