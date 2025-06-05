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
DB_HOST=XXXXXXXXXX
DB_PORT=1433
DB_NAME=XXXXXXXXXX
DB_USER=XXXXXXXXXX
DB_PASSWORD=XXXXXXXXXX
DB_DRIVER=ODBC Driver 18 for SQL Server
```