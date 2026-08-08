from src.ingest import load_trades
from src.validate import validate_trades
from src.process import categorize_trades
from src.database import (
    create_database,
    save_valid_trades,
    show_all_trades
)
from src.reports import (
    get_total_trades,
    get_total_quantity,
    get_average_price,
    get_trades_by_symbol,
    get_largest_trade
)


def main():
    """
    Run the financial trade processing pipeline.
    """

    print("=" * 50)
    print("Financial Trade Processing System")
    print("=" * 50)

    try:

        # --------------------------------
        # Step 1: Create database
        # --------------------------------

        create_database()

        # --------------------------------
        # Step 2: Load trade data
        # --------------------------------

        trades = load_trades(
            "data/trades.csv"
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
        # Step 3: Validate trades
        # --------------------------------

        validation_results = validate_trades(
            trades
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
        # Step 4: Categorize trades
        # --------------------------------

        valid_trades, invalid_trades = (
            categorize_trades(
                trades,
                validation_results
            )
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
        # Step 5: Display invalid trades
        # --------------------------------

        print("\nInvalid Trades")
        print("-" * 40)

        if invalid_trades.empty:

            print(
                "No invalid trades found."
            )

        else:

            print(invalid_trades)

        # --------------------------------
        # Step 6: Save valid trades
        # --------------------------------

        save_valid_trades(
            valid_trades
        )

        # --------------------------------
        # Step 7: Display database
        # --------------------------------

        show_all_trades()

        # --------------------------------
        # Step 8: Generate SQL reports
        # --------------------------------

        print("\n")
        print("=" * 50)
        print("SQL REPORTS")
        print("=" * 50)

        # Total trades

        total_trades = get_total_trades()

        print(
            f"\nTotal Trades: "
            f"{total_trades}"
        )

        # Total quantity

        total_quantity = get_total_quantity()

        print(
            f"Total Quantity: "
            f"{total_quantity}"
        )

        # Average price

        average_price = get_average_price()

        print(
            f"Average Price: "
            f"{average_price:.2f}"
        )

        # Trades by symbol

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

        # Largest trade

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

        print(
            "\nPipeline completed successfully."
        )

    except Exception as error:

        print(
            f"\nPipeline Failed: {error}"
        )


if __name__ == "__main__":
    main()