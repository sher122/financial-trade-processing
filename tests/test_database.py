import sqlite3

import pandas as pd

import src.database as database


def setup_test_database(monkeypatch, tmp_path):
    """
    Create an isolated SQLite database for testing.
    """

    test_database = tmp_path / "test_trades.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        test_database
    )

    database.create_database()

    return test_database


def create_trade_dataframe():
    """
    Create sample valid trade data.
    """

    return pd.DataFrame([
        {
            "trade_id": "T001",
            "symbol": "AAPL",
            "quantity": 100,
            "price": 185.50,
            "trade_date": "2026-08-01",
            "trader": "Alice",
        },
        {
            "trade_id": "T002",
            "symbol": "MSFT",
            "quantity": 50,
            "price": 420.75,
            "trade_date": "2026-08-01",
            "trader": "Bob",
        },
    ])


def test_create_database(monkeypatch, tmp_path):
    """
    Test that the database and required tables are created.
    """

    database_path = setup_test_database(
        monkeypatch,
        tmp_path
    )

    assert database_path.exists()

    with sqlite3.connect(database_path) as connection:

        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

    table_names = {
        table[0]
        for table in tables
    }

    assert "batches" in table_names
    assert "trades" in table_names
    assert "rejected_trades" in table_names


def test_create_batch(monkeypatch, tmp_path):
    """
    Test that a processing batch is created.
    """

    setup_test_database(
        monkeypatch,
        tmp_path
    )

    batch_id = database.create_batch(
        source_file="data/test.csv",
        total_records=10,
        valid_records=8,
        invalid_records=2,
    )

    assert batch_id == 1

    batch = database.get_batch(batch_id)

    assert batch is not None

    assert batch[0] == 1
    assert batch[1] == "data/test.csv"
    assert batch[3] == 10
    assert batch[4] == 8
    assert batch[5] == 2


def test_save_valid_trades(monkeypatch, tmp_path):
    """
    Test that valid trades are stored correctly.
    """

    setup_test_database(
        monkeypatch,
        tmp_path
    )

    batch_id = database.create_batch(
        source_file="data/test.csv",
        total_records=2,
        valid_records=2,
        invalid_records=0,
    )

    trades = create_trade_dataframe()

    inserted = database.save_valid_trades(
        batch_id,
        trades
    )

    assert inserted == 2

    with sqlite3.connect(database.DATABASE_PATH) as connection:

        count = connection.execute(
            """
            SELECT COUNT(*)
            FROM trades
            WHERE batch_id = ?
            """,
            (batch_id,)
        ).fetchone()[0]

    assert count == 2


def test_save_rejected_trades(monkeypatch, tmp_path):
    """
    Test that rejected trades are stored with their reasons.
    """

    setup_test_database(
        monkeypatch,
        tmp_path
    )

    batch_id = database.create_batch(
        source_file="data/test.csv",
        total_records=2,
        valid_records=1,
        invalid_records=1,
    )

    invalid_trades = pd.DataFrame([
        {
            "trade_id": "T003",
            "symbol": "GOOG",
            "quantity": -20,
            "price": 172.30,
            "trade_date": "2026-08-01",
            "trader": "Charlie",
        }
    ])

    validation_results = {
        "negative_quantity": invalid_trades
    }

    inserted = database.save_rejected_trades(
        batch_id,
        invalid_trades,
        validation_results
    )

    assert inserted == 1

    with sqlite3.connect(database.DATABASE_PATH) as connection:

        row = connection.execute(
            """
            SELECT
                trade_id,
                rejection_reason
            FROM rejected_trades
            WHERE batch_id = ?
            """,
            (batch_id,)
        ).fetchone()

    assert row == (
        "T003",
        "NEGATIVE QUANTITY"
    )


def test_batches_are_isolated(monkeypatch, tmp_path):
    """
    Test that trades from different batches remain separate.
    """

    setup_test_database(
        monkeypatch,
        tmp_path
    )

    batch_1 = database.create_batch(
        source_file="file1.csv",
        total_records=1,
        valid_records=1,
        invalid_records=0,
    )

    batch_2 = database.create_batch(
        source_file="file2.csv",
        total_records=1,
        valid_records=1,
        invalid_records=0,
    )

    trades_1 = pd.DataFrame([
        {
            "trade_id": "T001",
            "symbol": "AAPL",
            "quantity": 100,
            "price": 185.50,
            "trade_date": "2026-08-01",
            "trader": "Alice",
        }
    ])

    trades_2 = pd.DataFrame([
        {
            "trade_id": "T001",
            "symbol": "INFY",
            "quantity": 200,
            "price": 1845.50,
            "trade_date": "2026-08-02",
            "trader": "Aarav",
        }
    ])

    database.save_valid_trades(
        batch_1,
        trades_1
    )

    database.save_valid_trades(
        batch_2,
        trades_2
    )

    with sqlite3.connect(database.DATABASE_PATH) as connection:

        batch_1_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM trades
            WHERE batch_id = ?
            """,
            (batch_1,)
        ).fetchone()[0]

        batch_2_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM trades
            WHERE batch_id = ?
            """,
            (batch_2,)
        ).fetchone()[0]

    assert batch_1_count == 1
    assert batch_2_count == 1