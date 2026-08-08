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

    # Create the database directory if it doesn't exist
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Connect to SQLite
    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        # Create trades table
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

    Args:
        df: DataFrame containing valid trades.
    """

    if df.empty:
        print("\nNo valid trades to save.")
        return

    with sqlite3.connect(DATABASE_PATH) as connection:

        df.to_sql(
            name="trades",
            con=connection,
            if_exists="append",
            index=False
        )

    print(
        f"\n{len(df)} valid trades saved to database."
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