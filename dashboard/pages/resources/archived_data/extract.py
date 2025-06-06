"""Functions for extracting and caching the archived data."""
import pandas as pd


def load_data(file_name: str) -> pd.DataFrame:
    """Loading the data to a dataframe.
    Currently reads from a csv, can be changed to loading from RDS in future.
    """
    return pd.read_csv(file_name)


if __name__ == "__main__":
    df = load_data("test_plants_historical.csv")

    print(df.head())
    print(df.describe())
