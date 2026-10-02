import logging
import re

import pandas as pd


logger = logging.getLogger(__name__)


def show_overview(df):
    """Display basic information about a DataFrame."""
    logger.debug("DataFrame shape: %s", df.shape)

    print(f"Shape: {df.shape}")
    print("First five rows:")
    print(df.head())
    print(f"Columns: {list(df.columns)}")
    print("Data types:")
    print(df.dtypes)


def remove_duplicates(df):
    """Remove exact duplicate rows."""
    before = len(df)
    result = df.drop_duplicates()
    logger.debug(
        "Removed duplicate rows: %s before, %s after",
        before,
        len(result),
    )
    return result


def drop_missing_rows(df):
    """Remove rows containing missing values."""
    before = len(df)
    result = df.dropna()
    logger.debug(
        "Dropped rows with missing values: %s before, %s after",
        before,
        len(result),
    )
    return result


def clean_text(value):
    """Normalize one text value."""
    value = value.strip()
    value = value.lower()
    return re.sub(r"\s+", " ", value)


def remove_iqr_outliers(df, column, threshold):
    """Remove IQR outliers from one column."""
    if column not in df.columns:
        logger.error("Column not found: %s", column)
        raise ValueError(f"Column not found: {column}")

    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - threshold * iqr
    upper = q3 + threshold * iqr

    result = df[df[column].between(lower, upper)]
    logger.debug(
        "IQR bounds for %s: lower=%s, upper=%s; removed %s row(s)",
        column,
        lower,
        upper,
        len(df) - len(result),
    )
    return result
