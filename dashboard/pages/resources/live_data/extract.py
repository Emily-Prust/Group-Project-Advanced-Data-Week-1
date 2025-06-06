"""Functions for extracting and caching the live data."""

import pandas as pd


def get_mock_data(filepath: str) -> pd.DataFrame:
    """
    An example function used to load mock data.
    This doesn't need to be a function but having it
    helps show how the real data will flow.
    """
    return pd.read_csv(filepath)
