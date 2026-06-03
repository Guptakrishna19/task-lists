import argparse
import csv
from collections import defaultdict
from datetime import datetime


VALID_CATEGORIES = {"income", "food", "transport", "bills", "shopping", "other"}


def parse_args():
    parser = argparse.ArgumentParser(description="Create a monthly finance report from a CSV file.")
    parser.add_argument("--input", required=True, help="Path to the transactions CSV file.")
    parser.add_argument("--report", required=True, help="Path where the report should be saved.")
    return parser.parse_args()


def validate_row(row, line_number):
    required_fields = ["date", "description", "amount", "category"]

    for field in required_fields:
        if not row.get(field):
            return None, f"Line {line_number}: missing {field}"

    try:
        date = datetime.strptime(row["date"], "%Y-%m-%d")
    except ValueError:
        return None, f"Line {line_number}: invalid date '{row['date']}'"

    try:
        amount = float(row["amount"])
    except ValueError:
        return None, f"Line {line_number}: invalid amount '{row['amount']}'"

    category = row["category"].strip().lower()
    if category not in VALID_CATEGORIES:
        category = "other"

    transaction = {
        "date": date,
        "description": row["description"].strip(),
        "amount": amount,
        "category": category,
    }
    return transaction, None


def read_transactions(input_path):
    transactions = []
    errors = []

    with open(input_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for line_number, row in enumerate(reader, start=2):
            transaction, error = validate_row(row, line_number)

            if error:
                errors.append(error)
                continue

            transactions.append(transaction)

    return transactions, errors


def build_monthly_summary(transactions):
    summary = defaultdict(lambda: {"income": 0.0, "expenses": 0.0, "balance": 0.0})

    for transaction in transactions:
        month = transaction["date"].strftime("%Y-%m")
        amount = transaction["amount"]

        if amount >= 0:
            summary[month]["income"] += amount
        else:
            summary[month]["expenses"] += abs(amount)

        summary[month]["balance"] += amount

    return summary


def format_report(summary, errors):
    lines = ["Finance Tracker Report", "======================", ""]

    if summary:
        lines.append("Monthly Summary")
        lines.append("---------------")

        for month in sorted(summary):
            month_data = summary[month]
            lines.append(f"{month}")
            lines.append(f"  Income:   {month_data['income']:.2f}")
            lines.append(f"  Expenses: {month_data['expenses']:.2f}")
            lines.append(f"  Balance:  {month_data['balance']:.2f}")
            lines.append("")
    else:
        lines.append("No valid transactions found.")
        lines.append("")

    if errors:
        lines.append("Skipped Rows")
        lines.append("------------")
        lines.extend(errors)
        lines.append("")

    return "\n".join(lines)


def save_report(report_path, report_text):
    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report_text)


def main():
    args = parse_args()
    transactions, errors = read_transactions(args.input)
    summary = build_monthly_summary(transactions)
    report_text = format_report(summary, errors)
    save_report(args.report, report_text)

    print(f"Report saved to {args.report}")
    print(f"Valid transactions: {len(transactions)}")
    print(f"Skipped rows: {len(errors)}")


if __name__ == "__main__":
    main()
