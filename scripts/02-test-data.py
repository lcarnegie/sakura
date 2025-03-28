# ============= PREAMBLE =============
# Last Edited By: Luca Carnegie
# Date: March 28, 2025
# Description: 
#        - Tests clean data script by loading the cleaned data and checking for
#           missing values, duplicates, and basic statistics.
# ====================================

import os
import pandas as pd
import numpy as np
import pytest
from datetime import datetime

# Path to the data file (assuming it's in a relative location to the script)
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                         'data', 'analysis_data', 'flowering_data.csv')

def test_file_exists():
    """Test that the data file exists."""
    assert os.path.exists(DATA_PATH), f"Data file not found at {DATA_PATH}"

def test_data_can_be_loaded():
    """Test that the data can be loaded correctly."""
    df = pd.read_csv(DATA_PATH)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0, "DataFrame is empty"

def test_schema():
    """Test that the data has the expected columns."""
    df = pd.read_csv(DATA_PATH)
    expected_columns = ['year', 'flower_date', 'flower_doy', 'avg_temp_march_c']
    assert all(col in df.columns for col in expected_columns), "Missing expected columns"

def test_data_types():
    """Test that the columns have the expected data types."""
    df = pd.read_csv(DATA_PATH)
    
    # Test year is numeric
    assert pd.api.types.is_numeric_dtype(df['year']), "Year should be numeric"
    
    # Test flower_date is string when not NaN
    valid_dates = df['flower_date'].dropna()
    if len(valid_dates) > 0:
        assert pd.api.types.is_string_dtype(valid_dates), "flower_date should be string"
    
    # Test flower_doy and avg_temp_march_c are numeric
    numeric_cols = ['flower_doy', 'avg_temp_march_c']
    for col in numeric_cols:
        assert pd.api.types.is_numeric_dtype(df[col]), f"{col} should be numeric"

def test_value_ranges():
    """Test that values are within expected ranges."""
    df = pd.read_csv(DATA_PATH)
    
    # Year range
    assert df['year'].min() >= 800, "Year values are too low"
    assert df['year'].max() <= 1300, "Year values are too high"
    
    # DOY range (day of year)
    valid_doy = df['flower_doy'].dropna()
    if len(valid_doy) > 0:
        assert valid_doy.min() >= 1, "flower_doy should be at least 1"
        assert valid_doy.max() <= 366, "flower_doy should be at most 366"
    
    # Temperature range
    valid_temp = df['avg_temp_march_c'].dropna()
    if len(valid_temp) > 0:
        assert valid_temp.min() >= -5, "Temperature is unrealistically low"
        assert valid_temp.max() <= 25, "Temperature is unrealistically high"

def test_date_consistency():
    """Test that flower_date is consistent with year."""
    df = pd.read_csv(DATA_PATH)
    
    # Filter rows with both year and flower_date
    mask = df['flower_date'].notna()
    test_df = df[mask]
    
    if len(test_df) > 0:
        # Extract year from flower_date and compare with year column
        years_from_dates = test_df['flower_date'].str.split('-', expand=True)[0].astype(str)
        years_from_column = test_df['year'].astype(str)
        
        assert (years_from_dates == years_from_column).all(), "Years in flower_date don't match year column"

def test_doy_consistency():
    """Test that flower_doy is consistent with flower_date."""
    df = pd.read_csv(DATA_PATH)
    
    # Filter rows with both flower_date and flower_doy
    mask = df['flower_date'].notna() & df['flower_doy'].notna()
    test_df = df[mask]
    
    if len(test_df) > 0:
        for _, row in test_df.iterrows():
            date_str = row['flower_date']
            if pd.notna(date_str):
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    calculated_doy = date_obj.timetuple().tm_yday
                    assert abs(calculated_doy - row['flower_doy']) <= 1, f"DOY mismatch for {date_str}: calculated={calculated_doy}, recorded={row['flower_doy']}"
                except ValueError:
                    pytest.fail(f"Invalid date format: {date_str}")

def test_no_duplicates():
    """Test that there are no duplicate records."""
    df = pd.read_csv(DATA_PATH)
    assert df['year'].is_unique, "Duplicate years found in the dataset"

def test_report_missing_values():
    """Report on missing values in the dataset."""
    df = pd.read_csv(DATA_PATH)
    
    missing_counts = df.isna().sum()
    print(f"\nMissing value counts:\n{missing_counts}")
    
    # This isn't an assertion, just informational
    assert True