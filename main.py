import logging
import sys

from src.ingest import load_trades
from src.validate import validate_trades
from src.process import categorize_trades

from src.database import (
    create_database,
    create_batch,
    save_valid_trades,
    save_rejected_trades,
    show_batch_trades,
    show_batch_rejected_trades,
    show_all_batches
)

from src.reports import (
    get_batch_summary,
    get_total_trades,
    get_total_quantity,
    get_average_price,
    get_trades_by_symbol,
    get_largest_trade,
    export_trade_report,
    export_rejected_trade_report
)

from src.logger import setup_logger


def main():

    logger = setup_logger()

    print("=" * 60)
    print("Financial Trade Processing System")
    print("=" * 60)

    # --------------------------------
    # Command-line argument
    # --------------------------------

    if len(sys.argv) != 2:

        print(
            "\nUsage:"
        )

        print(
            "python main.py <input-file>"
        )

        print(
            "\nExamples:"
        )

        print(
            "python main.py data/trades.csv"
        )

        print(
            "python main.py data/trades_5000.xlsx"
        )

        return

    input_file = sys.argv[1]

    logger.info(
        f"Processing file: {input_file}"
    )

    try:

        # --------------------------------
        # Step 1: Create database
        # --------------------------------

        create_database()

        print(
            "\nDatabase initialized."
        )

        # --------------------------------
        # Step 2: Load data
        # --------------------------------

        trades = load_trades(
            input_file
        )

        print(
            "\nInput file loaded successfully."
        )

        print(
            f"Rows    : {trades.shape[0]}"
        )

        print(
            f"Columns : {trades.shape[1]}"
        )

        # --------------------------------
        # Step 3: Validate
        # --------------------------------

        validation_results = (
            validate_trades(trades)
        )

        print(
            "\nValidation Summary"
        )

        print(
            "-" * 40
        )

        for check_name, result in (
            validation_results.items()
        ):

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

        print(
            "\nTrade Processing Summary"
        )

        print(
            "-" * 40
        )

        print(
            f"Valid Trades   : "
            f"{len(valid_trades)}"
        )

        print(
            f"Invalid Trades : "
            f"{len(invalid_trades)}"
        )

        # --------------------------------
        # Step 5: Create batch
        # --------------------------------

        batch_id = create_batch(
            source_file=input_file,
            total_records=len(trades),
            valid_records=len(valid_trades),
            invalid_records=len(invalid_trades)
        )

        print(
            f"\nBatch ID: {batch_id}"
        )

        logger.info(
            f"Created batch {batch_id}"
        )

        # --------------------------------
        # Step 6: Save valid trades
        # --------------------------------

        inserted_valid = save_valid_trades(
            batch_id,
            valid_trades
        )

        print(
            f"Valid trades stored: "
            f"{inserted_valid}"
        )

        # --------------------------------
        # Step 7: Save rejected trades
        # --------------------------------

        inserted_rejected = (
            save_rejected_trades(
                batch_id,
                invalid_trades,
                validation_results
            )
        )

        print(
            f"Rejected records stored: "
            f"{inserted_rejected}"
        )

        # --------------------------------
        # Step 8: Display batch data
        # --------------------------------

        show_batch_trades(
            batch_id
        )

        show_batch_rejected_trades(
            batch_id
        )

        # --------------------------------
        # Step 9: Batch reports
        # --------------------------------

        print(
            "\nBatch Report"
        )

        print(
            "=" * 60
        )

        summary = get_batch_summary(
            batch_id
        )

        print(
            summary.to_string(
                index=False
            )
        )

        # --------------------------------
        # Step 10: SQL statistics
        # --------------------------------

        total_trades = get_total_trades(
            batch_id
        )

        total_quantity = get_total_quantity(
            batch_id
        )

        average_price = get_average_price(
            batch_id
        )

        print(
            f"\nTotal Trades   : "
            f"{total_trades}"
        )

        print(
            f"Total Quantity : "
            f"{total_quantity}"
        )

        print(
            f"Average Price  : "
            f"{average_price:.2f}"
        )

        # --------------------------------
        # Step 11: Symbol report
        # --------------------------------

        print(
            "\nTrades by Symbol"
        )

        print(
            "-" * 40
        )

        for row in get_trades_by_symbol(
            batch_id
        ):

            symbol = row[0]
            count = row[1]
            quantity = row[2]

            print(
                f"{symbol:<10}"
                f"Trades: {count:<5}"
                f"Quantity: {quantity}"
            )

        # --------------------------------
        # Step 12: Largest trade
        # --------------------------------

        largest_trade = get_largest_trade(
            batch_id
        )

        print(
            "\nLargest Trade"
        )

        print(
            "-" * 40
        )

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

        # --------------------------------
        # Step 13: Export reports
        # --------------------------------

        trade_report = (
            export_trade_report(
                batch_id
            )
        )

        rejected_report = (
            export_rejected_trade_report(
                batch_id
            )
        )

        print(
            "\nReports"
        )

        print(
            "-" * 40
        )

        print(
            f"Trade Report    : "
            f"{trade_report}"
        )

        print(
            f"Rejected Report : "
            f"{rejected_report}"
        )

        # --------------------------------
        # Step 14: Processing history
        # --------------------------------

        show_all_batches()

        logger.info(
            f"Batch {batch_id} completed."
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