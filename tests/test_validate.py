import pandas as pd

from src.validate import (
    check_duplicate_trades,
    check_negative_quantity,
    check_negative_price,
    check_missing_values,
    validate_trades
)


def create_test_trades():
    """
    Create a small DataFrame specifically for testing.
    """

    return pd.DataFrame([
        {
            "trade_id": "T001",
            "symbol": "AAPL",
            "quantity": 100,
            "price": 185.50,
            "trade_date": "2026-08-01",
            "trader": "Alice"
        },
        {
            "trade_id": "T002",
            "symbol": "MSFT",
            "quantity": 50,
            "price": 420.75,
            "trade_date": "2026-08-01",
            "trader": "Bob"
        },
        {
            "trade_id": "T003",
            "symbol": "GOOG",
            "quantity": -20,
            "price": 172.30,
            "trade_date": "2026-08-01",
            "trader": "Charlie"
        },
        {
            "trade_id": "T004",
            "symbol": "NVDA",
            "quantity": 10,
            "price": -950.00,
            "trade_date": "2026-08-01",
            "trader": "David"
        },
        {
            "trade_id": "T001",
            "symbol": "AAPL",
            "quantity": 100,
            "price": 185.50,
            "trade_date": "2026-08-01",
            "trader": "Alice"
        }
    ])


def test_duplicate_detection():

    trades = create_test_trades()

    duplicates = check_duplicate_trades(
        trades
    )

    assert len(duplicates) == 2

    assert set(
        duplicates["trade_id"]
    ) == {"T001"}


def test_negative_quantity_detection():

    trades = create_test_trades()

    invalid_quantity = (
        check_negative_quantity(trades)
    )

    assert len(invalid_quantity) == 1

    assert invalid_quantity.iloc[0]["trade_id"] == "T003"


def test_negative_price_detection():

    trades = create_test_trades()

    invalid_price = (
        check_negative_price(trades)
    )

    assert len(invalid_price) == 1

    assert invalid_price.iloc[0]["trade_id"] == "T004"


def test_missing_value_detection():

    trades = create_test_trades()

    trades.loc[0, "symbol"] = None

    missing_values = (
        check_missing_values(trades)
    )

    assert len(missing_values) == 1

    assert (
        missing_values.iloc[0]["trade_id"]
        == "T001"
    )


def test_validate_trades():

    trades = create_test_trades()

    results = validate_trades(
        trades
    )

    assert "duplicates" in results

    assert "negative_quantity" in results

    assert "negative_price" in results

    assert "missing_values" in results

    assert len(results["duplicates"]) == 2

    assert len(
        results["negative_quantity"]
    ) == 1

    assert len(
        results["negative_price"]
    ) == 1

    assert len(
        results["missing_values"]
    ) == 0