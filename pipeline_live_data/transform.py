"""Transforming the extracted data."""

import ast
import logging
import json

import pandas as pd

from extract import CSV_NAME

logger = logging.getLogger(__name__)

logging.basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def get_df_from_csv(filename: str) -> pd.DataFrame:
    """Returns a dataframe from the csv data."""
    logger.info("Reading CSV.")
    return pd.read_csv(filename)


def replace_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Drop and rename columns in a given dataframe."""

    df = df.drop(columns=['images'])
    logger.info("Columns dropped successfully.")
    df = df.rename(columns={
        'name': 'plant_name',
        'error': 'error_name',
        'recording_taken': 'at'
    })
    logger.info("Columns renamed successfully.")
    return df


def fix_type_of_string_dicts(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Changes the type of dict-like strings to dicts."""

    for col in cols:
        logger.info("Converting %s to dict.", col)
        df[col] = df[col].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else None)

    return df


def create_columns_from_dict_strings(orig_df: pd.DataFrame,
                                     new_df: pd.DataFrame, lookup_map: list[tuple]) -> pd.DataFrame:
    """
    Returns a dataframe with new columns, extracted from a
    dict in the original dataframe.
    Requires a list of tuples, with the tuples ordered as:
      (name_new_column, name_old_column, name_old_column_key).
    """

    for item in lookup_map:
        logger.info("Creating %s from dict.", item[0])

        new_df[item[0]] = orig_df[item[1]].apply(
            lambda x: x.get(item[2]) if isinstance(x, dict) else None
        )
    return new_df


def create_timestamps(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Returns a dataframe with columns converted to timestamps."""

    for col in cols:
        logger.info("Converting %s to timestamp.", col)
        df[col] = pd.to_datetime(df[col], utc=True)
    return df


def main_transform() -> pd.DataFrame:
    """Returns a clean and processed dataframe."""

    df = get_df_from_csv(CSV_NAME)

    df = replace_columns(df)
    df = fix_type_of_string_dicts(df, ['botanist', 'origin_location'])
    df['scientific_name'] = df['scientific_name'].str.strip(
        '[]').str.strip("'").str.strip('"')

    clean_df = df[['plant_id', 'plant_name', 'scientific_name', 'error_name', 'temperature',
                   'soil_moisture', 'last_watered', 'at', 'received_at']].copy()

    clean_df = create_columns_from_dict_strings(df, clean_df, [
        ('botanist_name', 'botanist', 'name'),
        ('botanist_email', 'botanist', 'email'),
        ('botanist_phone', 'botanist', 'phone'),
        ('origin_latitude', 'origin_location', 'latitude'),
        ('origin_longitude', 'origin_location', 'longitude'),
        ('city_name', 'origin_location', 'city'),
        ('country_name', 'origin_location', 'country')
    ])

    clean_df = create_timestamps(clean_df, ['at', 'received_at'])
    return clean_df


def create_separate_dfs(df: pd.DataFrame) -> tuple[pd.DataFrame]:
    """Returns separate dataframes based on the tables in the erd."""

    country_df = df[['country_name']].drop_duplicates()
    city_df = df[['city_name']].drop_duplicates()
    origin_df = df[['origin_latitude', 'origin_longitude']].drop_duplicates()
    plant_df = df[['plant_id', 'plant_name',
                   'scientific_name']].drop_duplicates()
    botanist_df = df[['botanist_name', 'botanist_email',
                      'botanist_phone']].drop_duplicates()
    error_df = df[['error_name']].drop_duplicates()

    return country_df, city_df, origin_df, plant_df, botanist_df, error_df


def create_json_from_dfs(df: pd.DataFrame) -> None:
    """Creates a json from the cleaned dataframe."""

    country_df, city_df, origin_df, plant_df, botanist_df, error_df = create_separate_dfs(
        df)

    # tables = {
    #     "Country": country_df.to_dict(orient='records'),
    #     "City": city_df.to_dict(orient='records'),
    #     "Origin": origin_df.to_dict(orient='records'),
    #     "Plant": plant_df.to_dict(orient='records'),
    #     "Botanist": botanist_df.to_dict(orient='records'),
    #     "Error": error_df.to_dict(orient='records')
    # }

    tables = {
        "Country": country_df.to_json(orient='records'),
        "City": city_df.to_json(orient='records'),
        "Origin": origin_df.to_json(orient='records'),
        "Plant": plant_df.to_json(orient='records'),
        "Botanist": botanist_df.to_json(orient='records'),
        "Error": error_df.to_json(orient='records')
    }

    with open('table_seed.json', 'w', encoding='utf-8') as f:
        json.dump(tables, f, indent=4)


if __name__ == "__main__":

    cleaned = main_transform()

    logger.info(cleaned.info())
    logger.info(cleaned.head())

    create_json_from_dfs(cleaned)
    # print(create_separate_dfs(cleaned))
