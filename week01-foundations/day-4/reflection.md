# Day 4 — OOP Fundamentals · Reflection

## What I built
- `src/banking.py` — `BankAccount` + `Transaction` + `OverdraftError` classes
- `tests/test_banking.py` — 39 unit tests, all passing

---

## Self-review

- **What was difficult:** Implementing `__eq__` correctly — had to handle the `isinstance` check and return `NotImplemented` (not `False`) when comparing against a non-Transaction type, which is a subtle but important distinction for Python's comparison protocol.

- **What was difficult:** Designing `OverdraftError` as a custom exception instead of a generic `ValueError` — understanding when to subclass `Exception` and why separating error types makes the API cleaner for callers who need to catch specific failures.

- **What was difficult:** Writing tests required more attention than expected — not just checking happy paths but proving that failed withdrawals leave balance unchanged, that `history()` returns a copy not a reference, and that read-only properties actually block writes.

- **Key insight:** `history()` returning `list(self._transactions)` instead of the raw internal list — a defensive copy ensures external code cannot mutate the account's state by holding a reference to its private data.

- **What remains:** Build a `SavingsAccount(BankAccount)` subclass with an interest rate and monthly interest application — to complete the inheritance side of today's objective.

---

## Honest self-assessment

`__init__` and `@property` — straightforward, no issues there. `__repr__` and `__eq__` needed real attention to get right. Custom exceptions and writing proper edge case tests were the parts that actually made me slow down and think. Inheritance is clear conceptually but needs more reps to feel natural.