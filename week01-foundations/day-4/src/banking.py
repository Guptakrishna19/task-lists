"""
banking.py — Day 4 OOP Fundamentals
Classes: Transaction, BankAccount, OverdraftError
"""

from datetime import datetime


# ─────────────────────────────────────────────
# Transaction class
# ─────────────────────────────────────────────

class Transaction:
    """Records a single deposit or withdrawal event."""

    VALID_TYPES = ("deposit", "withdrawal")

    def __init__(self, txn_type: str, amount: float, balance_after: float):
        if txn_type not in self.VALID_TYPES:
            raise ValueError(f"txn_type must be one of {self.VALID_TYPES}")
        if amount <= 0:
            raise ValueError("Transaction amount must be positive.")

        self.txn_type      = txn_type
        self.amount        = amount
        self.balance_after = balance_after
        self.timestamp     = datetime.now()

    def __repr__(self):
        sign   = "+" if self.txn_type == "deposit" else "-"
        ts_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"Transaction({self.txn_type}, {sign}Rs{self.amount:.2f}, "
            f"balance=Rs{self.balance_after:.2f}, at={ts_str})"
        )

    def __eq__(self, other):
        if not isinstance(other, Transaction):
            return NotImplemented
        return (
            self.txn_type      == other.txn_type
            and self.amount        == other.amount
            and self.balance_after == other.balance_after
            and self.timestamp     == other.timestamp
        )


# ─────────────────────────────────────────────
# Custom exception
# ─────────────────────────────────────────────

class OverdraftError(Exception):
    """Raised when a withdrawal would exceed the available balance."""
    pass


# ─────────────────────────────────────────────
# BankAccount class
# ─────────────────────────────────────────────

class BankAccount:
    """
    A simple bank account with deposit, withdrawal,
    overdraft protection, and full transaction history.

    Class attrs  : bank_name (shared), _count (total instances)
    Instance attrs: owner, _balance (via property), _transactions
    """

    bank_name = "PyBank"   # class attribute — shared by all accounts
    _count    = 0          # class attribute — total accounts created

    def __init__(self, owner: str, initial_balance: float = 0.0):
        if not owner or not isinstance(owner, str):
            raise ValueError("Owner must be a non-empty string.")
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")

        self.owner         = owner
        self._balance      = initial_balance
        self._transactions = []          # list[Transaction]

        BankAccount._count += 1

    # ── property ──────────────────────────────

    @property
    def balance(self) -> float:
        """Read-only access to current balance."""
        return self._balance

    # ── core methods ──────────────────────────

    def deposit(self, amount: float) -> Transaction:
        """
        Add funds to the account.
        Raises ValueError if amount <= 0.
        Returns the Transaction created.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        self._balance += amount
        txn = Transaction("deposit", amount, self._balance)
        self._transactions.append(txn)
        return txn

    def withdraw(self, amount: float) -> Transaction:
        """
        Remove funds from the account.
        Raises ValueError if amount <= 0.
        Raises OverdraftError if amount > balance.
        Returns the Transaction created.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            raise OverdraftError(
                f"Insufficient funds. "
                f"Tried to withdraw Rs{amount:.2f} but balance is Rs{self._balance:.2f}."
            )

        self._balance -= amount
        txn = Transaction("withdrawal", amount, self._balance)
        self._transactions.append(txn)
        return txn

    def history(self) -> list:
        """Return a copy of the full transaction history."""
        return list(self._transactions)

    def print_history(self) -> None:
        """Pretty-print all transactions to stdout."""
        if not self._transactions:
            print(f"[{self.owner}] No transactions yet.")
            return
        print(f"\n── Transaction History: {self.owner} ({BankAccount.bank_name}) ──")
        for i, txn in enumerate(self._transactions, start=1):
            print(f"  {i:>2}. {txn}")
        print(f"       Current balance : Rs{self._balance:.2f}\n")

    # ── class method ──────────────────────────

    @classmethod
    def total_accounts(cls) -> int:
        """Return total BankAccount instances ever created."""
        return cls._count

    # ── dunder methods ────────────────────────

    def __repr__(self):
        return (
            f"BankAccount(owner={self.owner!r}, "
            f"balance=Rs{self._balance:.2f}, "
            f"txns={len(self._transactions)})"
        )

    def __eq__(self, other):
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.owner == other.owner and self._balance == other._balance


# ─────────────────────────────────────────────
# Smoke test — only runs when executed directly
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Welcome to {BankAccount.bank_name}\n")

    acc = BankAccount("Arjun", initial_balance=1000.0)
    print(acc)

    acc.deposit(500)
    acc.deposit(250)
    acc.withdraw(200)

    try:
        acc.withdraw(99999)
    except OverdraftError as e:
        print(f"Overdraft blocked: {e}")

    acc.print_history()
    print(f"Total accounts ever created: {BankAccount.total_accounts()}")