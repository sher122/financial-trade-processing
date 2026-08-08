import pandas as pd


def check_duplicate_trades(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return all trades that have duplicate trade IDs.
    """

    return df[
        df.duplicated(
            subset="trade_id",
            keep=False
        )
    ]


def check_negative_quantity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return trades where quantity is less than or equal to zero.
    """

    return df[df["quantity"] <= 0]


def check_negative_price(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return trades where price is less than or equal to zero.
    """

    return df[df["price"] <= 0]


def check_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return trades containing missing values.
    """

    return df[df.isnull().any(axis=1)]


def validate_trades(df: pd.DataFrame) -> dict:
    """
    Run all trade validation checks.

    Returns:
        Dictionary containing the results of each validation check.
    """

    return {
        "duplicates": check_duplicate_trades(df),
        "negative_quantity": check_negative_quantity(df),
        "negative_price": check_negative_price(df),
        "missing_values": check_missing_values(df),
    }