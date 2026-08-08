import logging

from src.ingest import load_trades
from src.validate import validate_trades
from src.process import categorize_trades

from src.database import (
    create_database,
    save_valid_trades,
    save_rejected_trades,
    show_all_trades,
    show_rejected_trades
)

from src.reports import (
    get_total_trades,
    get_total_quantity,
    get_average_price,
    get_trades_by_symbol,
    get_largest_trade
)

from src.logger import setup_logger


def main():
    """
    Run the financial trade processing pipeline.
    """

    logger = setup_logger()

    logger.info("Pipeline started.")

    print("=" * 50)
    print("Financial Trade Processing System")
    print("=" * 50)

    try:

        # --------------------------------
        # Step 1: Create database
        # --------------------------------

        create_database()

        logger.info(
            "Database initialized."
        )

        # --------------------------------
        # Step 2: Load CSV
        # --------------------------------

        trades = load_trades(
            "data/trades.csv"
        )

        logger.info(
            f"CSV loaded: {len(trades)} trades."
        )

        print("\nCSV loaded successfully.\n")

        print(
            f"Rows    : {trades.shape[0]}"
        )

        print(
            f"Columns : {trades.shape[1]}"
        )

        print("\nColumn Names")

        for column in trades.columns:
            print(f"- {column}")

        print("\nFirst Five Trades\n")

        print(trades.head())

        # --------------------------------
        # Step 3: Validate
        # --------------------------------

        validation_results = validate_trades(
            trades
        )

        logger.info(
            "Trade validation completed."
        )

        print("\nValidation Summary")
        print("-" * 40)

        for check_name, result in validation_results.items():

            display_name = (
                check_name
                .replace("_", " ")
                .title()
            )

            print(
                f"{display_name:<25}"
                f"{len(result)}"
            )

        # --------------------------------
        # Step 4: Categorize
        # --------------------------------

        valid_trades, invalid_trades = (
            categorize_trades(
                trades,
                validation_results
            )
        )

        logger.info(
            f"Valid trades: {len(valid_trades)}"
        )

        logger.info(
            f"Invalid trades: {len(invalid_trades)}"
        )

        print("\nTrade Processing Summary")
        print("-" * 40)

        print(
            f"Valid Trades   : "
            f"{len(valid_trades)}"
        )

        print(
            f"Invalid Trades : "
            f"{len(invalid_trades)}"
        )

        # --------------------------------
        # Step 5: Save valid trades
        # --------------------------------

        save_valid_trades(
            valid_trades
        )

        logger.info(
            "Valid trades processed."
        )

        # --------------------------------
        # Step 6: Save rejected trades
        # --------------------------------

        save_rejected_trades(
            invalid_trades,
            validation_results
        )

        logger.info(
            "Rejected trades saved."
        )

        # --------------------------------
        # Step 7: Display database
        # --------------------------------

        show_all_trades()

        show_rejected_trades()

        # --------------------------------
        # Step 8: SQL Reports
        # --------------------------------

        print("\n")
        print("=" * 50)
        print("SQL REPORTS")
        print("=" * 50)

        total_trades = get_total_trades()

        print(
            f"\nTotal Trades: "
            f"{total_trades}"
        )

        total_quantity = get_total_quantity()

        print(
            f"Total Quantity: "
            f"{total_quantity}"
        )

        average_price = get_average_price()

        print(
            f"Average Price: "
            f"{average_price:.2f}"
        )

        trades_by_symbol = (
            get_trades_by_symbol()
        )

        print("\nTrades by Symbol")
        print("-" * 40)

        for row in trades_by_symbol:

            symbol = row[0]
            trade_count = row[1]
            total_quantity = row[2]

            print(
                f"{symbol:<10}"
                f"Trades: {trade_count:<5}"
                f"Quantity: {total_quantity}"
            )

        largest_trade = get_largest_trade()

        print("\nLargest Trade")
        print("-" * 40)

        if largest_trade:

            (
                trade_id,
                symbol,
                quantity,
                price,
                trade_date,
                trader
            ) = largest_trade

            print(
                f"Trade ID : {trade_id}"
            )

            print(
                f"Symbol   : {symbol}"
            )

            print(
                f"Quantity : {quantity}"
            )

            print(
                f"Price    : {price}"
            )

            print(
                f"Date     : {trade_date}"
            )

            print(
                f"Trader   : {trader}"
            )

        else:

            print("No trades found.")

        logger.info(
            "Reports generated."
        )

        logger.info(
            "Pipeline completed successfully."
        )

        print(
            "\nPipeline completed successfully."
        )

    except Exception as error:

        logger.exception(
            "Pipeline failed."
        )

        print(
            f"\nPipeline Failed: {error}"
        )


if __name__ == "__main__":
    main()