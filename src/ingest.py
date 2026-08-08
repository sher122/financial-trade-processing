from pathlib import Path

import pandas as pd


def load_trades(file_path: str) -> pd.DataFrame:
    """
    Load trade data from a CSV file.

    Args:
        file_path: Path to the CSV file.

    Returns:
        A pandas DataFrame containing the trade data.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the CSV file is empty.
    """

    csv_path = Path(file_path)

    if not csv_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {csv_path}"
        )

    try:
        dataframe = pd.read_csv(csv_path)

        if dataframe.empty:
            raise ValueError("CSV file is empty.")

        return dataframe

    except pd.errors.EmptyDataError:
        raise ValueError("CSV file contains no data.")

    except pd.errors.ParserError as error:
        raise ValueError(
            f"Unable to parse CSV file: {error}"
        )