import sqlite3
from pathlib import Path

import pandas as pd

from src.database import DATABASE_PATH


REPORTS_DIRECTORY = Path("reports")


def get_batch_summary(batch_id):
    """
    Return summary information for a batch.
    """

    with sqlite3.connect(DATABASE_PATH) as connection:

        dataframe = pd.read_sql_query(
            """
            SELECT
                batch_id,
                source_file,
                processed_at,
                total_records,
                valid_records,
                invalid_records
            FROM batches
            WHERE batch_id = ?
            """,
            connection,
            params=(batch_id,)
        )

    return dataframe


def get_total_trades(batch_id):
    """
    Return number of valid trades in a batch.
    """

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM trades
            WHERE batch_id = ?
        """, (batch_id,))

        return cursor.fetchone()[0]


def get_total_quantity(batch_id):
    """
    Return total quantity for a batch.
    """

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT SUM(quantity)
            FROM trades
            WHERE batch_id = ?
        """, (batch_id,))

        result = cursor.fetchone()[0]

    return result or 0


def get_average_price(batch_id):
    """
    Return average trade price for a batch.
    """

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT AVG(price)
            FROM trades
            WHERE batch_id = ?
        """, (batch_id,))

        result = cursor.fetchone()[0]

    return result or 0


def get_trades_by_symbol(batch_id):
    """
    Return trade statistics grouped by symbol.
    """

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                symbol,
                COUNT(*) AS trade_count,
                SUM(quantity) AS total_quantity
            FROM trades
            WHERE batch_id = ?
            GROUP BY symbol
            ORDER BY total_quantity DESC
        """, (batch_id,))

        return cursor.fetchall()


def get_largest_trade(batch_id):
    """
    Return the largest trade in a batch.
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
            ORDER BY quantity DESC
            LIMIT 1
        """, (batch_id,))

        return cursor.fetchone()


def export_trade_report(batch_id):
    """
    Export valid trades for a batch.
    """

    REPORTS_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = (
        REPORTS_DIRECTORY /
        f"batch_{batch_id}_trade_report.csv"
    )

    with sqlite3.connect(DATABASE_PATH) as connection:

        dataframe = pd.read_sql_query(
            """
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
            """,
            connection,
            params=(batch_id,)
        )

    dataframe.to_csv(
        output_path,
        index=False
    )

    return output_path


def export_rejected_trade_report(batch_id):
    """
    Export rejected trades for a batch.
    """

    REPORTS_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = (
        REPORTS_DIRECTORY /
        f"batch_{batch_id}_rejected_trade_report.csv"
    )

    with sqlite3.connect(DATABASE_PATH) as connection:

        dataframe = pd.read_sql_query(
            """
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
            """,
            connection,
            params=(batch_id,)
        )

    dataframe.to_csv(
        output_path,
        index=False
    )

    return output_path