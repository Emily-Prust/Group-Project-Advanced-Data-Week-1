"""Transform script.

TEMPORARY:
Extracting gives us:
- a pandas dataframe containing plant data, extracted once an hour
- bound by anything older than (current time - 24 / 23 hours) -> 24 hours at most in rds?
    - calculated from the received_at and recording_taken columns

Assuming we have a dataframe... :
"""


from datetime import datetime, timedelta, timezone
import pandas as pd


def get_file_data() -> dict:
    """Returns a dict of file specific data."""

    current_time = datetime.now(timezone.utc)
    start_window = current_time - timedelta(hours=24)
    year = start_window.strftime('%Y')
    month = start_window.strftime('%m')
    day = start_window.strftime('%d')

    filename = f'plants_{start_window.strftime('%H_%d-%m-%Y')}.csv'

    return {
        "start_window": start_window,
        "file_name": filename,
        "bucket_key": f"{year}/{month}/{day}/{filename}"
    }


if __name__ == "__main__":
    print(get_file_data())
