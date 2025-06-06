# `/pipeline_archived_data`

## Setup

Run the following command in a terminal to download the necessary driver:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18 mssql-tools18
```

Create a `.env` with the following keys:

```
DB_HOST=[DATABASE HOST]
DB_PORT=1433
DB_NAME=[DATABASE NAME]
DB_USER=[DATABASE USERNAME]
DB_PASSWORD=[DATABASE PASSWORD]
DB_DRIVER=ODBC Driver 18 for SQL Server

BUCKET_NAME=[NAME OF S3 BUCKET]
AWS_ACCESS_KEY=[AWS ACCESS KEY ID]
AWS_SECRET_KEY=[AWS SECRET KEY ID]
```

## Files

### extract.py

Extracts data from an RDS, connected to via credentials in the `.env` file.
Grabs a snapshot of the timestamp we are interested in, and collects the extracted 
data into pandas DataFrame alongside it.  

### transform.py

Creates a CSV file from the extracted data, and returns the dictionary containing 
the filename and the path to upload in S3.

### load.py

Calls the extract and transform process, and loads the created CSV into a defined S3 bucket.