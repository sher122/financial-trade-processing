# Financial Trade Processing System

A Python-based batch processing system for ingesting, validating, categorizing, storing, and reporting financial trade data.

The project simulates a simplified trade-processing workflow in which CSV files are processed as independent batches. Valid trades are persisted to SQLite, while invalid trades are retained separately with rejection reasons for auditability.

---

## Overview

The system processes trade files through the following workflow:

```text
CSV Input
    |
    v
CSV Ingestion
    |
    v
Schema Normalization
    |
    v
Data Validation
    |
    v
Trade Categorization
    |
    v
Batch Creation
    |
    +----------------------+
    |                      |
    v                      v
Valid Trades          Invalid Trades
    |                      |
    v                      v
trades table        rejected_trades table
    |                      |
    +----------+-----------+
               |
               v
        Batch Reports
               |
               v
      Processing Summary
```

---
## Why This Project

Financial institutions process large volumes of trade records and need reliable controls around data ingestion, validation, storage, and auditability before records move to downstream systems. This project simulates that ingestion-and-control layer by processing trade files as independent batches, validating data-quality rules, separating valid and rejected records, persisting results in a relational database, and generating reports for review.
---
---
## Features

### CSV Ingestion

The system accepts trade data from CSV files.

**Required columns:**

- `trade_id`
- `symbol`
- `quantity`
- `price`
- `trade_date`
- `trader`

**The ingestion layer:**

- Verifies that the input file exists
- Ensures that the input file is a CSV
- Loads the data using Pandas
- Normalizes column names
- Validates the required schema
- Normalizes symbols and text fields
- Converts quantity and price to numeric values
- Normalizes trade dates

### Trade Validation

The validation layer checks incoming trades for common data-quality problems.

**Current validation rules:**

- Duplicate trade IDs
- Negative quantities
- Negative prices
- Missing values

Invalid records are separated from valid records and retained in the database with rejection information.

**Example validation output:**

```text
Validation Summary
----------------------------------------
Duplicates                8
Negative Quantity         5
Negative Price            5
Missing Values            4
```

### Trade Categorization

After validation, trades are separated into two DataFrames:

- Valid Trades
- Invalid Trades

A trade is considered invalid if its row appears in one or more validation results.

This keeps the processing logic separate from the individual validation rules.

### Batch Processing

Each input file is processed as a separate batch.

**A batch records:**

- Batch ID
- Source file
- Processing timestamp
- Total records
- Valid records
- Invalid records

**Example:**

```text
Batch ID: 5

Total Records  : 30
Valid Records  : 30
Invalid Records: 0
```
```
## Example SQL Queries

The database layer uses SQL directly through Python's `sqlite3` module.
### Retrieve Trades for a Batch
The system retrieves valid trades belonging to a specific processing batch:

```sql
SELECT
    trade_id,
    symbol,
    quantity,
    price,
    trade_date,
    trader
FROM trades
WHERE batch_id = ?
ORDER BY trade_id;
```
Batch IDs allow multiple input files to be processed while keeping their results separate.

---

## Database

The project currently uses SQLite for local persistence.

The database contains three main tables:

- `batches`
- `trades`
- `rejected_trades`

### `batches`

Stores metadata about each processing run.

- `batch_id`
- `source_file`
- `processed_at`
- `total_records`
- `valid_records`
- `invalid_records`

### `trades`

Stores valid trades.

- `batch_id`
- `trade_id`
- `symbol`
- `quantity`
- `price`
- `trade_date`
- `trader`

The table uses:

```text
(batch_id, trade_id)
```

as its primary key.

This allows the same `trade_id` to appear in different processing batches.

For example:

```text
Batch 1 -> T001 -> AAPL
Batch 2 -> T001 -> INFY
```

These records can coexist because they belong to different batches.

### `rejected_trades`

Stores rejected records and their rejection reasons.

- `rejection_id`
- `batch_id`
- `trade_id`
- `symbol`
- `quantity`
- `price`
- `trade_date`
- `trader`
- `rejection_reason`

This provides an audit trail for records that failed validation.

---

## Reporting

The system generates CSV reports for processed batches.

**Reports include:**

- Valid trade report
- Rejected trade report

Reports are generated under the `reports/` directory.

Generated reports are excluded from Git version control because they are outputs of the pipeline rather than source files.

---

## Example

The project has been tested with both small and larger CSV datasets.

### 30-Record Example

A sample dataset containing 30 Indian-market trades includes fields such as:

```csv
trade_id,symbol,quantity,price,trade_date,trader
T001,CIPLA,85,1582.45,2026-08-06,Madhuri
T002,SBIN,250,812.45,2026-08-01,Neha
T003,HINDALCO,190,742.55,2026-08-05,Manish
```

The pipeline produced:

```text
Input file loaded successfully.
Rows    : 30
Columns : 6

Valid Trades   : 30
Invalid Trades : 0
```

The system then stored the 30 valid trades under the corresponding processing batch.

### 5,000-Record Example

The pipeline was also tested with a 5,000-row dataset containing intentionally invalid records.

**Example validation result:**

```text
Rows    : 5000
Columns : 6

Duplicates                8
Negative Quantity         5
Negative Price            5
Missing Values            4

Valid Trades   : 4978
Invalid Trades : 22
```
### Example Rejected Trade Report

The pipeline generates a rejected-trade CSV containing the original trade information and the reason the record failed validation.

Example:

```csv
trade_id,symbol,quantity,price,trade_date,trader,rejection_reason
T001,AAPL,100,185.5,2026-08-01,Alice,DUPLICATES
T003,GOOG,-20,172.3,2026-08-01,Charlie,NEGATIVE QUANTITY
T004,NVDA,10,-950.0,2026-08-01,David,NEGATIVE PRICE

The valid and rejected records were persisted separately.

---
```
## Project Structure

```text
Financial-Trade-Processing/
|
├── data/
│   ├── trades.csv
│   └── india_trades_30.csv
|
├── database/
│   └── trades.db
|
├── reports/
│   └── generated reports
|
├── src/
│   ├── __init__.py
│   ├── ingest.py
│   ├── validate.py
│   ├── process.py
│   ├── database.py
│   └── reports.py
|
├── tests/
│   ├── test_ingest.py
│   ├── test_process.py
│   ├── test_validate.py
│   └── test_database.py
|
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

---

## Technologies

- Python 3.9
- Pandas
- SQLite
- SQL
- Pytest
- Git

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Financial-Trade-Processing
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment:

```bash
.\.venv\Scripts\Activate
```

If PowerShell execution policies prevent activation, the virtual environment can still be used directly:

```bash
.\.venv\Scripts\python.exe
```

### 3. Install dependencies

```bash
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## Running the Pipeline

The input CSV file is supplied as a command-line argument.

**Example:**

```bash
.\.venv\Scripts\python.exe main.py data\trades.csv
```

For the included 30-row sample:

```bash
.\.venv\Scripts\python.exe main.py data\india_trades_30.csv
```

**The pipeline performs:**

1. Load CSV
2. Normalize input
3. Validate trades
4. Categorize valid and invalid records
5. Create processing batch
6. Store valid trades
7. Store rejected trades
8. Generate reports
9. Display processing statistics

---

## Testing

The project uses Pytest for automated testing.

Run the complete test suite:

```bash
.\.venv\Scripts\python.exe -m pytest -v
```

**The test suite covers the following areas.**

### Ingestion Tests

- Successful CSV loading
- Missing input files
- Empty CSV files
- Column-name normalization
- Symbol and trader normalization
- Date normalization
- Numeric conversion
- Missing required columns
- Non-CSV input

### Processing Tests

- Separation of valid and invalid trades

### Validation Tests

- Duplicate trade detection
- Negative quantity detection
- Negative price detection
- Missing-value detection

### Database Tests

- Database creation
- Required table creation
- Batch creation
- Valid trade insertion
- Rejected trade insertion
- Batch isolation

**Current test suite:**

```text
15 ingestion/processing/validation tests
5 database tests
----------------------------
20 tests
```

**Expected result:**

```text
20 passed
```

---

## Batch Isolation

One important database design requirement is keeping processing batches independent.

For example:

```text
Batch 1
T001 -> AAPL

Batch 2
T001 -> INFY
```

Both records can exist because the database identifies a trade using:

```text
(batch_id, trade_id)
```

rather than `trade_id` alone.

This prevents records from different processing runs from conflicting with one another.

---

## Data Flow Example

Given an input file containing 30 records:

```text
30 input records
       |
       v
   Validation
       |
   +---+---+
   |       |
   v       v
 30 valid  0 invalid
   |       |
   v       v
trades   rejected_trades
   |
   v
Reports
```

For a file containing invalid records:

```text
5000 input records
        |
        v
    Validation
        |
    +---+---+
    |       |
    v       v
 4978      22
 valid    invalid
    |       |
    v       v
 trades  rejected_trades
```

---

## Error Handling

The ingestion layer provides explicit errors for common input problems.

**Missing File**

```text
CSV file not found: <path>
```

**Empty File**

```text
CSV file is empty.
```

**Missing Required Column**

```text
Missing column: trader
```

**Unsupported File Type**

```text
Only CSV files are supported.
```

---

## Design

The project separates responsibilities across modules.

```text
ingest.py
    |
    |-- Load and normalize input
    |
validate.py
    |
    |-- Apply validation rules
    |
process.py
    |
    |-- Categorize valid/invalid trades
    |
database.py
    |
    |-- Persist batches and trades
    |
reports.py
    |
    |-- Generate processing reports
    |
main.py
    |
    |-- Orchestrate the pipeline
```

This separation makes individual components easier to test and modify.

---

## Current Scope

The current implementation supports:

- CSV input
- Data normalization
- Trade validation
- Valid/invalid trade categorization
- Batch processing
- SQLite persistence
- Rejected-trade storage
- Batch history
- CSV reporting
- Automated testing

---

## Current Limitations

This project is a simplified financial trade-processing implementation and is not a production trading or settlement system.

**Current limitations include:**

- CSV is the only supported input format
- SQLite is currently used for persistence
- No real-time trade ingestion
- No external market-data integration
- No reference-dataset reconciliation
- No trade settlement processing
- No authentication or authorization
- No distributed processing
- No production monitoring

---

## Future Improvements

Potential future development includes:

- End-to-end pipeline tests
- Reference-dataset reconciliation
- MySQL/PostgreSQL support
- SQL-based analytics
- Improved audit logging
- Configuration management
- Structured application logging
- Performance testing with larger datasets
- Docker support
- CI/CD using GitHub Actions
- Database migrations
- Production monitoring

---

## What This Project Demonstrates

This project demonstrates practical experience with:

- Python application development
- Pandas data processing
- CSV-based ETL workflows
- Data-quality validation
- SQL and relational database design
- SQLite persistence
- Batch processing
- Audit-oriented rejected-record handling
- Automated testing with Pytest
- Git/GitHub version control
- Modular application architecture
- Error handling and input validation

---

## Project Status

| Component | Status |
|---|---|
| CSV ingestion | Complete |
| Input normalization | Complete |
| Data validation | Complete |
| Trade categorization | Complete |
| Batch processing | Complete |
| SQLite persistence | Complete |
| Rejected trade storage | Complete |
| Batch history | Complete |
| CSV reporting | Complete |
| Automated tests | Complete |
| Reference-data reconciliation | Not implemented |
| MySQL/PostgreSQL support | Planned |
| End-to-end testing | Planned |

---

## Disclaimer

This project is an educational simulation of a financial trade-processing workflow.

It is not intended for use in actual trading, settlement, accounting, or other production financial systems.
