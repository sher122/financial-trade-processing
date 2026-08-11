# Financial Trade Processing System

A Python-based batch processing system for ingesting, validating, categorizing, storing, and reporting financial trade data.

The project simulates a simplified trade-processing workflow in which CSV files are processed as independent batches. Valid trades are persisted to SQLite, while invalid trades are retained separately with rejection reasons for auditability.

---

## Overview

The system processes trade files through the following workflow:

CSV Input
   ↓
CSV Ingestion
   ↓
Schema Normalization
   ↓
Data Validation
   ↓
Trade Categorization
   ↓
Batch Creation
   ↓
┌─────────────────────┬──────────────────────┐
│                     │                      │
Valid Trades       Invalid Trades             │
│                     │                      │
↓                     ↓                      │
trades table      rejected_trades table     │
│                     │                      │
└──────────────┬──────┴──────────────────────┘
               ↓
          Batch Reports
               ↓
        Processing Summary

---

## Features

### CSV Ingestion

The system accepts trade data from CSV files.

Required columns:

```text
trade_id
symbol
quantity
price
trade_date
trader
