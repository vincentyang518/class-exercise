import logging


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
