import sqlite3

from src.database import DATABASE_PATH


def get_total_trades():
    """
    Return the total number of trades in the database.
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
    Return the total quantity of all trades.
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
    Return the average trade price.
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
    Return trade count and total quantity grouped by symbol.
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

        result = cursor.fetchone()

    return result