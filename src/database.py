import sqlite3
from pathlib import Path

import pandas as pd


DATABASE_PATH = Path("database/trades.db")


def create_database():
    """
    Create the database and all required tables.
    """

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        # --------------------------------
        # Batches
        # --------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS batches (
                batch_id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_file TEXT NOT NULL,
                processed_at TEXT NOT NULL,
                total_records INTEGER NOT NULL,
                valid_records INTEGER NOT NULL,
                invalid_records INTEGER NOT NULL
            )
        """)

        # --------------------------------
        # Valid trades
        # --------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                batch_id INTEGER NOT NULL,
                trade_id TEXT NOT NULL,
                symbol TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                trade_date TEXT NOT NULL,
                trader TEXT NOT NULL,

                PRIMARY KEY (
                    batch_id,
                    trade_id
                ),

                FOREIGN KEY (
                    batch_id
                )
                REFERENCES batches(batch_id)
            )
        """)

        # --------------------------------
        # Rejected trades
        # --------------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rejected_trades (
                rejection_id INTEGER PRIMARY KEY AUTOINCREMENT,

                batch_id INTEGER NOT NULL,
                trade_id TEXT NOT NULL,
                symbol TEXT,
                quantity INTEGER,
                price REAL,
                trade_date TEXT,
                trader TEXT,

                rejection_reason TEXT NOT NULL,

                FOREIGN KEY (
                    batch_id
                )
                REFERENCES batches(batch_id)
            )
        """)

        connection.commit()


def create_batch(
    source_file,
    total_records,
    valid_records,
    invalid_records
):
    """
    Create a new processing batch.

    Returns the generated batch ID.
    """

    from datetime import datetime

    processed_at = datetime.now().isoformat(
        timespec="seconds"
    )

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO batches (
                source_file,
                processed_at,
                total_records,
                valid_records,
                invalid_records
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            source_file,
            processed_at,
            total_records,
            valid_records,
            invalid_records
        ))

        batch_id = cursor.lastrowid

        connection.commit()

    return batch_id


def save_valid_trades(
    batch_id,
    df: pd.DataFrame
):
    """
    Save valid trades belonging to a batch.
    """

    if df.empty:
        return 0

    inserted_count = 0

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        for _, trade in df.iterrows():

            cursor.execute("""
                INSERT INTO trades (
                    batch_id,
                    trade_id,
                    symbol,
                    quantity,
                    price,
                    trade_date,
                    trader
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                batch_id,
                trade["trade_id"],
                trade["symbol"],
                trade["quantity"],
                trade["price"],
                trade["trade_date"],
                trade["trader"]
            ))

            inserted_count += 1

        connection.commit()

    return inserted_count


def save_rejected_trades(
    batch_id,
    invalid_trades: pd.DataFrame,
    validation_results: dict
):
    """
    Save rejected trades belonging to a batch.

    Every rejected input row is preserved.
    """

    if invalid_trades.empty:
        return 0

    inserted_count = 0

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        for index, trade in invalid_trades.iterrows():

            reasons = []

            for check_name, result in validation_results.items():

                if index in result.index:

                    reason = (
                        check_name
                        .replace("_", " ")
                        .upper()
                    )

                    reasons.append(reason)

            for rejection_reason in reasons:

                cursor.execute("""
                    INSERT INTO rejected_trades (
                        batch_id,
                        trade_id,
                        symbol,
                        quantity,
                        price,
                        trade_date,
                        trader,
                        rejection_reason
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    batch_id,
                    trade["trade_id"],
                    trade["symbol"],
                    trade["quantity"],
                    trade["price"],
                    trade["trade_date"],
                    trade["trader"],
                    rejection_reason
                ))

                inserted_count += 1

        connection.commit()

    return inserted_count


def get_batch(batch_id):
    """
    Return information about a specific batch.
    """

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                batch_id,
                source_file,
                processed_at,
                total_records,
                valid_records,
                invalid_records
            FROM batches
            WHERE batch_id = ?
        """, (batch_id,))

        return cursor.fetchone()


def show_batch_trades(batch_id):
    """
    Display valid trades for a batch.
    """

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                trade_id,
                symbol,
                quantity,
                price,
                trade_date,
                trader
            FROM trades
            WHERE batch_id = ?
            ORDER BY trade_id
        """, (batch_id,))

        rows = cursor.fetchall()

    print("\nTrades for Batch", batch_id)
    print("-" * 70)

    if not rows:
        print("No valid trades found.")
        return

    for row in rows:
        print(row)


def show_batch_rejected_trades(batch_id):
    """
    Display rejected trades for a batch.
    """

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                trade_id,
                symbol,
                quantity,
                price,
                trade_date,
                trader,
                rejection_reason
            FROM rejected_trades
            WHERE batch_id = ?
            ORDER BY rejection_id
        """, (batch_id,))

        rows = cursor.fetchall()

    print("\nRejected Trades for Batch", batch_id)
    print("-" * 70)

    if not rows:
        print("No rejected trades found.")
        return

    for row in rows:
        print(row)


def show_all_batches():
    """
    Display all processed batches.
    """

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                batch_id,
                source_file,
                processed_at,
                total_records,
                valid_records,
                invalid_records
            FROM batches
            ORDER BY batch_id
        """)

        rows = cursor.fetchall()

    print("\nProcessing History")
    print("-" * 80)

    if not rows:
        print("No batches found.")
        return

    for row in rows:
        print(row)