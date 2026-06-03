# Day 6 Task - Finance Tracker CLI

This task builds a command-line finance tracker that reads transactions from a CSV file and exports a monthly report.

## Files

- `finance_tracker.py` - the CLI program
- `sample_transactions.csv` - sample input data with valid and bad rows
- `report.txt` - generated output after running the program

## CSV Format

The input CSV should have these columns:

```text
date,description,amount,category
```

Example:

```text
2026-06-01,Salary,50000,income
2026-06-02,Groceries,-1200,food
```

Valid categories are:

```text
income, food, transport, bills, shopping, other
```

Unknown categories are changed to `other`.

## Usage

Run from the `day-6` folder:

```bash
python finance_tracker.py --input sample_transactions.csv --report report.txt
```

Or run from the project root:

```bash
python week01-foundations/day-6/finance_tracker.py --input week01-foundations/day-6/sample_transactions.csv --report week01-foundations/day-6/report.txt
```

## What It Does

1. Reads transactions from a CSV file.
2. Skips bad rows without crashing.
3. Groups valid transactions by month.
4. Calculates income, expenses, and balance.
5. Saves the report to a text file.

## Error Handling

The program handles these bad rows:

- Missing required fields
- Invalid dates
- Invalid amounts

Skipped rows are listed at the end of the generated report.

## Reflection

- I practiced using `argparse` for command-line inputs.
- I used `csv.DictReader` to read structured data.
- I handled bad rows by collecting errors instead of stopping the program.
- I grouped transactions by month and exported a readable report.
