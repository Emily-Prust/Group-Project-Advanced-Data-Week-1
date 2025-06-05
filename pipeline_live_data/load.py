"""Uploading the transformed data."""
"""Uploading the transformed data."""

"""

Thought process:
- Begin by mapping out the different jobs this script has to do.
- Then diagram/function signatures.
- Write tests to ensure data is being moved appropriately
  (closer to how it needs to be in the database).

Link to diagramming:
https://www.tldraw.com/f/doKFMmlKMKrPYSz0X3VeU?d=v-656.-100.2868.2808.jDrHNUxqQJRuDwIhCEf5g


REQUIREMENTS:
- Connect to the database.

INPUT:
- (From transform) data in the following form:
    - pandas dataframe with lots of columns.

FUNCTION:
- Split these columns into the necessary tables.
- Pull in existing information regarding:

    Inserting into Plant and the left side of the ERD should be rare.

    Measurement and Plant_Error will update frequently.
    These primarily depend on Plant & Error.

    Initial checks should be for Plant and Error only.

OUTPUT/ROLE:
- Upload data to the following tables (order matters):
    - Error
    - Plant_Error
    - Measurement
    - Botanist
    - Botanist_Assignment
    - Country
    - City
    - Origin
    - Plant

TO DO LIST:
- Function signatures.
- Tests.
- Logging.
- Write code.
- Refactor.
- Ask for a code review.

"""

if __name__ == "__main__":
    pass
