transactions = [
    {
        "date": "2026-06-01",
        "description": "Salary",
        "amount": "50000",
        "category": "income",
    },
    {
        "date": "2026-06-02",
        "description": "Groceries",
        "amount": "-1200",
        "category": "food",
    },
    {
        "date": "2026-06-03",
        "description": "Bus pass",
        "amount": "-800",
        "category": "transport",
    },
]

for transaction in transactions:
    print(transaction["description"], transaction["amount"])
