"""Transforming the extracted data."""

import ast
import pandas as pd

from extract import CSV_NAME


def get_df_from_csv(filename: str) -> pd.DataFrame:
    """Returns a dataframe from the csv data."""
    return pd.read_csv(filename)


def replace_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Drop and rename columns in a given dataframe."""

    df = df.drop(columns=['images'])
    df = df.rename(columns={
        'name': 'plant_name',
        'error': 'error_name',
        'recording_taken': 'at'
    })
    return df


def fix_type_of_string_dicts(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Changes the type of dict-like like strings to dicts."""

    for col in cols:
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
        # log here, mapping item[0] ..

        new_df[item[0]] = orig_df[item[1]].apply(
            lambda x: x.get(item[2]) if isinstance(x, dict) else None
        )
    return new_df


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

    return clean_df


if __name__ == "__main__":

    cleaned = main_transform()

    print(cleaned.info())
    print(cleaned['scientific_name'].head(50))
    print(cleaned.head(10))
