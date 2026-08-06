from pathlib import Path
import pandas as pd


def load_trades(file_path: str) -> pd.DataFrame:
    """
    Load trade data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded trade data.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If the CSV file is empty.
    """

    csv_path = Path(file_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    try:
        dataframe = pd.read_csv(csv_path)

        if dataframe.empty:
            raise ValueError("CSV file is empty.")

        return dataframe

    except Exception as error:
        raise Exception(f"Error reading CSV: {error}")