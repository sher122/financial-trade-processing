import sqlite3
from pathlib import Path

import pandas as pd


DATABASE_PATH = Path("database/trades.db")


def create_database():
    """
    Create the SQLite database and required tables.
    """

    print("Creating database...")

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        # -----------------------------
        # Valid trades table
        # -----------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                trade_id TEXT PRIMARY KEY,
                symbol TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                trade_date TEXT NOT NULL,
                trader TEXT NOT NULL
            )
        """)

        # -----------------------------
        # Rejected trades table
        # -----------------------------

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rejected_trades (
                rejection_id INTEGER PRIMARY KEY AUTOINCREMENT,
                trade_id TEXT,
                symbol TEXT,
                quantity INTEGER,
                price REAL,
                trade_date TEXT,
                trader TEXT,
                rejection_reason TEXT NOT NULL
            )
        """)

        connection.commit()

    print("Database created successfully.")


def save_valid_trades(df: pd.DataFrame):
    """
    Save valid trades into the SQLite database.

    Existing trade IDs are skipped.
    """

    if df.empty:
        print("\nNo valid trades to save.")
        return

    inserted_count = 0
    skipped_count = 0

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        for _, trade in df.iterrows():

            try:

                cursor.execute("""
                    INSERT INTO trades (
                        trade_id,
                        symbol,
                        quantity,
                        price,
                        trade_date,
                        trader
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    trade["trade_id"],
                    trade["symbol"],
                    trade["quantity"],
                    trade["price"],
                    trade["trade_date"],
                    trade["trader"]
                ))

                inserted_count += 1

            except sqlite3.IntegrityError:

                skipped_count += 1

        connection.commit()

    print(
        f"\nInserted trades : {inserted_count}"
    )

    print(
        f"Skipped trades  : {skipped_count}"
    )


def save_rejected_trades(
    invalid_trades: pd.DataFrame,
    validation_results: dict
):
    """
    Save invalid trades and their rejection reasons.
    """

    if invalid_trades.empty:
        print("\nNo rejected trades to save.")
        return

    rejection_records = []

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

        rejection_reason = ", ".join(reasons)

        rejection_records.append({
            "trade_id": trade["trade_id"],
            "symbol": trade["symbol"],
            "quantity": trade["quantity"],
            "price": trade["price"],
            "trade_date": trade["trade_date"],
            "trader": trade["trader"],
            "rejection_reason": rejection_reason
        })

    rejected_df = pd.DataFrame(
        rejection_records
    )

    with sqlite3.connect(DATABASE_PATH) as connection:

        rejected_df.to_sql(
            name="rejected_trades",
            con=connection,
            if_exists="append",
            index=False
        )

    print(
        f"\nRejected trades saved: "
        f"{len(rejected_df)}"
    )


def show_all_trades():
    """
    Display all valid trades stored in the database.
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
            ORDER BY trade_date, trade_id
        """)

        rows = cursor.fetchall()

    print("\nTrades Stored in Database")
    print("-" * 60)

    if not rows:
        print("No trades found.")
        return

    for row in rows:
        print(row)


def show_rejected_trades():
    """
    Display rejected trades and their reasons.
    """

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                trade_id,
                symbol,
                quantity,
                price,
                rejection_reason
            FROM rejected_trades
            ORDER BY rejection_id
        """)

        rows = cursor.fetchall()

    print("\nRejected Trades")
    print("-" * 60)

    if not rows:
        print("No rejected trades found.")
        return

    for row in rows:
        print(row)