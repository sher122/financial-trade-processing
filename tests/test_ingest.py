import pandas as pd
import pytest

from src.ingest import load_trades


def test_load_trades_successfully(tmp_path):
    """
    Test that a valid CSV file is loaded correctly.
    """

    csv_file = tmp_path / "trades.csv"

    csv_file.write_text(
        "trade_id,symbol,quantity,price,trade_date,trader\n"
        "T001,AAPL,100,185.50,2026-08-01,Alice\n"
        "T002,MSFT,50,420.75,2026-08-01,Bob\n"
    )

    trades = load_trades(str(csv_file))

    assert isinstance(trades, pd.DataFrame)

    assert len(trades) == 2

    assert list(trades.columns) == [
        "trade_id",
        "symbol",
        "quantity",
        "price",
        "trade_date",
        "trader",
    ]


def test_load_trades_file_not_found():
    """
    Test that a missing CSV file raises FileNotFoundError.
    """

    with pytest.raises(FileNotFoundError):
        load_trades("does_not_exist.csv")


def test_load_empty_csv(tmp_path):
    """
    Test that an empty CSV raises ValueError.
    """

    csv_file = tmp_path / "empty.csv"

    csv_file.write_text("")

    with pytest.raises(ValueError):
        load_trades(str(csv_file))


def test_load_trades_normalizes_column_names(tmp_path):
    """
    Test that column names are stripped and converted to lowercase.
    """

    csv_file = tmp_path / "trades.csv"

    csv_file.write_text(
        " Trade_ID , SYMBOL , Quantity , Price , Trade_Date , Trader \n"
        "T001,AAPL,100,185.50,2026-08-01,Alice\n"
    )

    trades = load_trades(str(csv_file))

    assert list(trades.columns) == [
        "trade_id",
        "symbol",
        "quantity",
        "price",
        "trade_date",
        "trader",
    ]


def test_load_trades_normalizes_symbol_and_trader(tmp_path):
    """
    Test that symbol is uppercase and text fields are stripped.
    """

    csv_file = tmp_path / "trades.csv"

    csv_file.write_text(
        "trade_id,symbol,quantity,price,trade_date,trader\n"
        " T001 , aapl ,100,185.50,2026-08-01, Alice \n"
    )

    trades = load_trades(str(csv_file))

    assert trades.loc[0, "trade_id"] == "T001"
    assert trades.loc[0, "symbol"] == "AAPL"
    assert trades.loc[0, "trader"] == "Alice"


def test_load_trades_normalizes_dates(tmp_path):
    """
    Test that valid dates are converted to YYYY-MM-DD.
    """

    csv_file = tmp_path / "trades.csv"

    csv_file.write_text(
        "trade_id,symbol,quantity,price,trade_date,trader\n"
        "T001,AAPL,100,185.50,08/01/2026,Alice\n"
    )

    trades = load_trades(str(csv_file))

    assert trades.loc[0, "trade_date"] == "2026-08-01"


def test_load_trades_converts_numeric_columns(tmp_path):
    """
    Test that quantity and price are converted to numeric values.
    """

    csv_file = tmp_path / "trades.csv"

    csv_file.write_text(
        "trade_id,symbol,quantity,price,trade_date,trader\n"
        "T001,AAPL,100,185.50,2026-08-01,Alice\n"
    )

    trades = load_trades(str(csv_file))

    assert trades.loc[0, "quantity"] == 100
    assert trades.loc[0, "price"] == 185.50

    assert pd.api.types.is_numeric_dtype(
        trades["quantity"]
    )

    assert pd.api.types.is_numeric_dtype(
        trades["price"]
    )


def test_load_trades_missing_column(tmp_path):
    """
    Test that a CSV missing a required column raises ValueError.
    """

    csv_file = tmp_path / "trades.csv"

    csv_file.write_text(
        "trade_id,symbol,quantity,price,trade_date\n"
        "T001,AAPL,100,185.50,2026-08-01\n"
    )

    with pytest.raises(
        ValueError,
        match="Missing column.*trader"
    ):
        load_trades(str(csv_file))


def test_load_trades_rejects_non_csv(tmp_path):
    """
    Test that non-CSV files are rejected.
    """

    file_path = tmp_path / "trades.txt"

    file_path.write_text(
        "trade_id,symbol,quantity,price,trade_date,trader\n"
    )

    with pytest.raises(
        ValueError,
        match="Only CSV files are supported"
    ):
        load_trades(str(file_path))