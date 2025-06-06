# Provided the correct credentials are in the .env, connect to the database.
source .env
sqlcmd -S $DB_HOST,$DB_PORT -U $DB_USER -P $DB_PASSWORD -d $DB_NAME