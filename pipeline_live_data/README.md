# `/pipeline_live_data`

## Setup 

- Create a `.venv`
- Install requirements `pip install -r requirements.txt`
- Brew install `unixodbc` as in [Dan's notes](https://github.com/Peritract/pymssql-example/tree/main/pyodbc%20example)
- Create a `.env` file and add the following values:  
```
DB_HOST=[DATABASE HOST]
DB_PORT=1433
DB_USER=[DATABASE USERNAME]
DB_PASSWORD=[DATABASE PASSWORD]
DB_NAME=[DATABASE NAME]
DB_SCHEMA=[DATABASE SCHEMA]
DB_DRIVER=ODBC Driver 18 for SQL Server
```

## Running

To run the pipeline, run `load.py` which calls both the `extract.py` and `transform.py` scripts, pulling data from an API, processing it and uploading it to an AWS RDS.

## Files

### extract.py

Extracts plant data asynchronously from an API endpoint, and outputs it to a csv file. When rerun, appends new data to that same csv file.

### transform.py

Creates a pandas DataFrame from the csv file and processes it, preparing it for upload.

### load.py

Uploads the DataFrame to an RDS as specified by the `.env` credentials.

### connect.sh

Allows for connecting to the database based on the credentials in the `.env` locally.

### Test files

Run with `pytest`, which tests basic functionality of the pipeline. Always expect all to pass.

### seed_database.py

Seeds the database initially, by inserting static data into it, and building the foreign connections.