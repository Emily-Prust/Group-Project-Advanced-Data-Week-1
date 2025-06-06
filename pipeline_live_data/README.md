# `/pipeline_live_data`

TEMPORARY DEV LOG:
List of columns dropped:
- 'images'
- 'botanist'
- 'origin_location'

List of columns renamed:
- 'name' -> 'plant_name'
- 'error' -> 'error_name'
- 'recording_taken' -> 'at'

List of new columns:
- 'botanist_name'
- 'botanist_email'
- 'botanist_phone'
- 'origin_latitude'
- 'origin_longitude'
- 'city_name'
- 'country_name'

Setup steps:
- New venv
- Get requirements
- Brew install `unixodbc` as in [Dan's notes](https://github.com/Peritract/pymssql-example/tree/main/pyodbc%20example)
- Make a .env file
