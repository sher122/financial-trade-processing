# Financial Trade Processing System

A Python-based financial trade processing pipeline that simulates the daily processing of trade data.
The system reads trade data from CSV files, validates and categorizes trades, stores the results in SQLite, generates reports, and maintains processing history using batch IDs.
The project is designed to simulate concepts found in real-world financial data processing workflows.

---

## Project Overview

Financial institutions process large numbers of trades every day.
A typical workflow involves:

1. Receiving trade data
2. Loading the data
3. Validating the records
4. Detecting invalid trades
5. Separating valid and rejected trades
6. Storing the results in a database
7. Generating reports
8. Maintaining an audit trail of processing batches

This project implements a simplified version of that workflow.
---

## Features
Trade Validation

The system checks incoming trades for common data-quality problems.

Current validation checks include:

Duplicate trade IDs
Negative quantities
Negative prices
Missing values

Invalid trades are separated from valid trades.


Batch Processing

Each input file is treated as a processing batch.

Every batch records:

Batch ID
Source file
Processing timestamp
Total records
Valid records
Invalid records

SQLite Database

The system uses SQLite for persistent storage.

The database contains three main tables:

batches
trades
rejected_trades
batches

Stores information about each processing run.

trades

Stores valid trades.

The primary key is:

(batch_id, trade_id)

This allows the same trade ID to appear in different processing batches.

rejected_trades

Stores invalid trades together with their rejection reason.



Technologies
Python 3.9
Pandas
SQLite
SQL
Pytest
Git
PowerShell

### CSV Ingestion
trader
