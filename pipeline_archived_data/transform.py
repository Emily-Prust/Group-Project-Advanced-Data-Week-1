"""Transform script.

TEMPORARY:
Extracting gives us:
- a pandas dataframe containing plant data, extracted once an hour
- bound by anything older than (current time - 24 / 23 hours) -> 24 hours at most in rds?
    - calculated from the received_at and recording_taken columns

Assuming we have a dataframe... :
"""


if __name__ == "__main__":
    pass
