from src.ingest import load_trades
from src.validate import validate_trades
from src.process import categorize_trades


def main():
    print("=" * 50)
    print("Financial Trade Processing System")
    print("=" * 50)

    try:
        # Load trade data
        trades = load_trades("data/trades.csv")

        print("\nCSV loaded successfully.\n")

        print(f"Rows    : {trades.shape[0]}")
        print(f"Columns : {trades.shape[1]}")

        print("\nColumn Names")
        for column in trades.columns:
            print(f"- {column}")

        print("\nFirst Five Trades\n")
        print(trades.head())

        # ----------------------------
        # Validation
        # ----------------------------
        validation_results = validate_trades(trades)

        print("\nValidation Summary")
        print("-" * 40)

        for check_name, result in validation_results.items():
            print(f"{check_name.replace('_', ' ').title():<25} {len(result)}")

        # ----------------------------
        # Categorize Trades
        # ----------------------------
        valid_trades, invalid_trades = categorize_trades(
            trades,
            validation_results
        )

        print("\nTrade Processing Summary")
        print("-" * 40)
        print(f"Valid Trades   : {len(valid_trades)}")
        print(f"Invalid Trades : {len(invalid_trades)}")

        print("\nInvalid Trades")
        print("-" * 40)

        if invalid_trades.empty:
            print("No invalid trades found.")
        else:
            print(invalid_trades)

    except Exception as error:
        print(f"\nPipeline Failed: {error}")


if __name__ == "__main__":
    main()