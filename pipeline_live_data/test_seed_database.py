"""Tests for functions used in seeding the plant data to the DB."""
# pylint: skip-file

import pytest
import pandas as pd

from seed_database import get_error_information


def test_get_error_information_1():
    """Check that get_error_information returns relevant information."""
    # Opportunity to test this. Requires a test dataframe (fixture ideally).
    assert True
