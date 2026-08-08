import pandas as pd

from src.process import categorize_trades


def test_categorize_trades():

    trades = pd.DataFrame([
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
        }
    ])

    validation_results = {
        "negative_quantity": trades[
            trades["quantity"] < 0
        ]
    }

    valid_trades, invalid_trades = (
        categorize_trades(
            trades,
            validation_results
        )
    )

    assert len(valid_trades) == 2

    assert len(invalid_trades) == 1

    assert (
        invalid_trades.iloc[0]["trade_id"]
        == "T003"
    )

    assert set(
        valid_trades["trade_id"]
    ) == {"T001", "T002"}