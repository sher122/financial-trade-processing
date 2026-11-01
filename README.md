# Financial Trade Processing System

A Python pipeline that simulates daily trade processing: it reads trade data from CSV files, validates each record, separates valid and rejected trades, stores the results in SQLite, and keeps an audit trail of every processing run using batch IDs.

## Overview

Financial institutions process large numbers of trades every day. A typical workflow looks like this:

1. Receive trade data
2. Load the data
3. Validate each record
4. Detect invalid trades
5. Separate valid and rejected trades
6. Store the results in a database
7. Generate reports
8. Keep an audit trail of processing batches

This project implements a simplified version of that workflow.

## Features

### Trade validation

Each incoming trade is checked for common data-quality problems:

- Duplicate trade IDs
- Negative quantities
- Negative prices
- Missing values

Invalid trades are separated from valid ones instead of being silently dropped.

### Batch processing

Each input file is treated as one processing batch. Every batch records:

- Batch ID
- Source file
- Processing timestamp
- Total records
- Valid records
- Invalid records

### SQLite persistence

Results are stored in a SQLite database with three tables:

| Table | Purpose |
|---|---|
| `batches` | One row per processing run (batch ID, source file, timestamp, record counts) |
| `trades` | Valid trades, linked to the batch that loaded them |
| `rejected_trades` | Invalid trades, with the reason for rejection |

The primary key of `trades` is `(batch_id, trade_id)`, so the same trade ID can appear in different batches without conflict.

## Technologies

Python 3.9, pandas, SQLite, SQL, pytest, Git

## Project Structure

```
financial-trade-processing/
├── data/            # input CSV files
├── src/             # processing modules
├── tests/           # pytest tests
├── main.py          # entry point
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/sher122/financial-trade-processing.git
cd financial-trade-processing
pip install -r requirements.txt
```

## Usage

Run the pipeline:

```bash
python main.py
```

## Running the tests

```bash
python -m pytest -v
```

The tests cover:

- Duplicate trade ID detection
- Negative quantity and price handling
- Missing value handling

## Example queries

Once a batch has been processed, the database can be queried directly.

Rejected trades per batch:

```sql
SELECT batch_id, COUNT(*) AS rejected_count
FROM rejected_trades
GROUP BY batch_id;
```

## Limitations

- Validation covers a fixed set of checks (duplicates, negative values, missing values).


## Disclaimer

This project is for educational and software-engineering demonstration purposes only.
