from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "trade_id",
    "symbol",
    "quantity",
    "price",
    "trade_date",
    "trader",
]


def load_trades(file_path: str) -> pd.DataFrame:
    """
    Load and normalize trade data from a CSV file.

    Steps:
    1. Check that the file exists.
    2. Check that it is a CSV file.
    3. Read the CSV.
    4. Normalize column names.
    5. Validate the required schema.
    6. Normalize trade dates.
    7. Return a cleaned DataFrame.
    """

    csv_path = Path(file_path)

    # --------------------------------
    # File existence
    # --------------------------------

    if not csv_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {csv_path}"
        )

    # --------------------------------
    # File type
    # --------------------------------

    if csv_path.suffix.lower() != ".csv":
        raise ValueError(
            f"Unsupported file type: {csv_path.suffix}. "
            "Only CSV files are supported."
        )

    try:

        # --------------------------------
        # Read CSV
        # --------------------------------

        dataframe = pd.read_csv(csv_path)

        if dataframe.empty:
            raise ValueError(
                "CSV file is empty."
            )

        # --------------------------------
        # Normalize column names
        # --------------------------------

        dataframe.columns = (
            dataframe.columns
            .str.strip()
            .str.lower()
        )

        # --------------------------------
        # Validate schema
        # --------------------------------

        actual_columns = set(
            dataframe.columns
        )

        required_columns = set(
            REQUIRED_COLUMNS
        )

        missing_columns = (
            required_columns - actual_columns
        )

        extra_columns = (
            actual_columns - required_columns
        )

        if missing_columns:

            missing = ", ".join(
                sorted(missing_columns)
            )

            raise ValueError(
                "Invalid input schema. "
                f"Missing column(s): {missing}. "
                "Expected columns: "
                f"{', '.join(REQUIRED_COLUMNS)}"
            )

        if extra_columns:

            extra = ", ".join(
                sorted(extra_columns)
            )

            print(
                "Warning: ignoring unexpected "
                f"column(s): {extra}"
            )

        # --------------------------------
        # Keep only expected columns
        # --------------------------------

        dataframe = dataframe[
            REQUIRED_COLUMNS
        ].copy()

        # --------------------------------
        # Normalize trade ID and symbol
        # --------------------------------

        dataframe["trade_id"] = (
            dataframe["trade_id"]
            .astype("string")
            .str.strip()
        )

        dataframe["symbol"] = (
            dataframe["symbol"]
            .astype("string")
            .str.strip()
            .str.upper()
        )

        dataframe["trader"] = (
            dataframe["trader"]
            .astype("string")
            .str.strip()
        )

        # --------------------------------
        # Normalize numeric columns
        # --------------------------------

        dataframe["quantity"] = pd.to_numeric(
            dataframe["quantity"],
            errors="coerce"
        )

        dataframe["price"] = pd.to_numeric(
            dataframe["price"],
            errors="coerce"
        )

        # --------------------------------
        # Normalize dates
        # --------------------------------

        dataframe["trade_date"] = pd.to_datetime(
            dataframe["trade_date"],
            errors="coerce"
        ).dt.strftime("%Y-%m-%d")

        return dataframe

    except pd.errors.EmptyDataError:

        raise ValueError(
            "CSV file contains no data."
        )

    except pd.errors.ParserError as error:

        raise ValueError(
            f"Unable to parse CSV file: {error}"
        )