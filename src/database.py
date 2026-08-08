import sqlite3
from pathlib import Path

import pandas as pd


DATABASE_PATH = Path("database/trades.db")


def create_database():
    """
    Create the SQLite database and trades table
    if they do not already exist.
    """

    print("Creating database...")

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

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


def show_all_trades():
    """
    Display all trades currently stored in the database.
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