# Day 6 Exercise - Finance Tracker Practice

This folder is for practicing the pieces of the Finance Tracker CLI before building the final project.

## What the exercise line means

The notebook says:

> argparse CLI; read transactions CSV; categorize; monthly summary; export report

That means we will practice these five smaller skills:

1. `argparse CLI`
   - Make a Python file that can accept values from the terminal.
   - Example later:
     ```bash
     python finance_tracker.py --input transactions.csv --report report.txt
     ```

2. `read transactions CSV`
   - Read a CSV file containing money records.
   - Example columns:
     ```text
     date,description,amount,category
     2026-06-01,Salary,50000,income
     2026-06-02,Groceries,-1200,food
     ```

3. `categorize`
   - Put each transaction into a category such as `income`, `food`, `transport`, `bills`, or `shopping`.

4. `monthly summary`
   - Group transactions by month.
   - Example: for `2026-06`, calculate income, expenses, and balance.

5. `export report`
   - Save the final summary into a file instead of only printing it.

## Step 1

Start with `exercise_01_transactions.py`.

Run:

```bash
python exercise_01_transactions.py
```

Expected result:

```text
Salary 50000
Groceries -1200
Bus pass -800
```
