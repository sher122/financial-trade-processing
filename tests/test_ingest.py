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
        "trader"
    ]


def test_load_trades_file_not_found():
    """
    Test that a missing CSV file raises FileNotFoundError.
    """

    with pytest.raises(FileNotFoundError):

        load_trades(
            "does_not_exist.csv"
        )


def test_load_empty_csv(tmp_path):
    """
    Test that an empty CSV raises ValueError.
    """

    csv_file = tmp_path / "empty.csv"

    csv_file.write_text("")

    with pytest.raises(ValueError):

        load_trades(str(csv_file))