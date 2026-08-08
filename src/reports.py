import sqlite3
from pathlib import Path

import pandas as pd

from src.database import DATABASE_PATH


REPORTS_DIRECTORY = Path("reports")


def get_total_trades():
    """
    Return the total number of valid trades.
    """

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM trades
        """)

        result = cursor.fetchone()

    return result[0]


def get_total_quantity():
    """
    Return total quantity of valid trades.
    """

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT SUM(quantity)
            FROM trades
        """)

        result = cursor.fetchone()

    return result[0] or 0


def get_average_price():
    """
    Return average trade price.
    """

    with sqlite3.connect(DATABASE_PATH) as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT AVG(price)
            FROM trades
        """)

        result = cursor.fetchone()

    return result[0] or 0


def get_trades_by_symbol():
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
            GROUP BY symbol
            ORDER BY total_quantity DESC
        """)

        results = cursor.fetchall()

    return results


def get_largest_trade():
    """
    Return the trade with the largest quantity.
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
            ORDER BY quantity DESC
            LIMIT 1
        """)

        return cursor.fetchone()


def export_trade_report():
    """
    Export all valid trades to a CSV file.
    """

    REPORTS_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = (
        REPORTS_DIRECTORY /
        "daily_trade_report.csv"
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
            ORDER BY trade_date, trade_id
            """,
            connection
        )

    dataframe.to_csv(
        output_path,
        index=False
    )

    return output_path


def export_rejected_trade_report():
    """
    Export rejected trades and their reasons
    to a CSV file.
    """

    REPORTS_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = (
        REPORTS_DIRECTORY /
        "rejected_trade_report.csv"
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
            ORDER BY rejection_id
            """,
            connection
        )

    dataframe.to_csv(
        output_path,
        index=False
    )

    return output_path