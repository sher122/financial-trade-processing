import pandas as pd


def categorize_trades(df: pd.DataFrame, validation_results: dict):
    """
    Split trades into valid and invalid DataFrames.
    """

    invalid_indexes = set()

    for result in validation_results.values():
        invalid_indexes.update(result.index.tolist())

    invalid_trades = df.loc[sorted(invalid_indexes)].copy()

    valid_trades = df.drop(index=invalid_indexes).copy()

    return valid_trades, invalid_trades