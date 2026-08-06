from src.ingest import load_trades


def main():
    print("=" * 50)
    print("Financial Trade Processing System")
    print("=" * 50)

    try:
        trades = load_trades("data/trades.csv")

        print("\nCSV loaded successfully.\n")

        print(f"Rows    : {trades.shape[0]}")
        print(f"Columns : {trades.shape[1]}")

        print("\nColumn Names")

        for column in trades.columns:
            print(f"- {column}")

        print("\nFirst Five Trades\n")

        print(trades.head())

    except Exception as error:
        print(f"\nPipeline Failed: {error}")


if __name__ == "__main__":
    main()