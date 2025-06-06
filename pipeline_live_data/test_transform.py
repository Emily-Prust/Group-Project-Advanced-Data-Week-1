"""Testing functions in transform.py ."""
# pylint: skip-file

import pytest
import pandas as pd

from transform import replace_columns, fix_type_of_string_dicts, create_timestamps


@pytest.fixture
def test_df():
    return pd.DataFrame({
        'name': ['Croton', pd.NA],
        'error': [pd.NA, 'plant sensor fault'],
        'recording_taken': ['2025-06-03T14:26:10.367Z', pd.NA],
        'botanist': ["{'name': 'Jo Baumbach', 'email': 'jo.baumbach@lnhm.co.uk', 'phone': '976-364-3090'}", pd.NA],
        'images': ["image", pd.NA]
    })


def test_replace_columns_column_names_change_as_expected(test_df):
    """Testing column names are renamed appropriately."""

    df = replace_columns(test_df)
    assert list(df.columns) == ['plant_name', 'error_name', 'at', 'botanist']


def test_fix_type_of_string_dicts_col_data_type_changes(test_df):
    """Testing the type of a column changes."""

    assert isinstance(test_df.loc[0, 'botanist'], str)
    df = fix_type_of_string_dicts(test_df, ['botanist'])
    assert isinstance(df.loc[0, 'botanist'], dict)


def test_create_timestamps_changes_data_type(test_df):
    """Testing string is converted to datetime."""

    assert isinstance(test_df.loc[0, 'recording_taken'], str)
    df = create_timestamps(test_df, ['recording_taken'])
    assert isinstance(test_df.loc[0, 'recording_taken'], pd.Timestamp)
