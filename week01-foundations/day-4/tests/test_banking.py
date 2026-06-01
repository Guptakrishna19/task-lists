"""
test_banking.py — Unit tests for banking.py
Covers: normal cases + edge/error cases
Run with: python -m pytest tests/ -v  OR  python tests/test_banking.py
"""

import unittest
from src.banking import BankAccount, Transaction, OverdraftError


class TestTransaction(unittest.TestCase):

    def test_deposit_transaction_created_correctly(self):
        txn = Transaction("deposit", 500.0, 1500.0)
        self.assertEqual(txn.txn_type, "deposit")
        self.assertEqual(txn.amount, 500.0)
        self.assertEqual(txn.balance_after, 1500.0)

    def test_withdrawal_transaction_created_correctly(self):
        txn = Transaction("withdrawal", 200.0, 800.0)
        self.assertEqual(txn.txn_type, "withdrawal")
        self.assertEqual(txn.amount, 200.0)
        self.assertEqual(txn.balance_after, 800.0)

    def test_invalid_txn_type_raises(self):
        with self.assertRaises(ValueError):
            Transaction("transfer", 100.0, 900.0)

    def test_zero_amount_raises(self):
        with self.assertRaises(ValueError):
            Transaction("deposit", 0, 1000.0)

    def test_negative_amount_raises(self):
        with self.assertRaises(ValueError):
            Transaction("deposit", -50, 1000.0)

    def test_repr_contains_key_info(self):
        txn = Transaction("deposit", 300.0, 1300.0)
        r = repr(txn)
        self.assertIn("deposit", r)
        self.assertIn("300.00", r)
        self.assertIn("1300.00", r)

    def test_eq_same_values(self):
        txn1 = Transaction("deposit", 100.0, 600.0)
        txn2 = Transaction("deposit", 100.0, 600.0)
        # timestamps differ by microseconds — eq only true if same object
        # equality based on all fields including timestamp
        self.assertEqual(txn1, txn1)
        self.assertNotEqual(txn1, txn2)  # timestamps differ

    def test_eq_wrong_type(self):
        txn = Transaction("deposit", 100.0, 600.0)
        self.assertNotEqual(txn, "not a transaction")


class TestBankAccountCreation(unittest.TestCase):

    def test_default_balance_is_zero(self):
        acc = BankAccount("Priya")
        self.assertEqual(acc.balance, 0.0)

    def test_initial_balance_set(self):
        acc = BankAccount("Raj", initial_balance=5000.0)
        self.assertEqual(acc.balance, 5000.0)

    def test_owner_set(self):
        acc = BankAccount("Meera")
        self.assertEqual(acc.owner, "Meera")

    def test_empty_owner_raises(self):
        with self.assertRaises(ValueError):
            BankAccount("")

    def test_negative_initial_balance_raises(self):
        with self.assertRaises(ValueError):
            BankAccount("Someone", initial_balance=-100)

    def test_balance_is_read_only(self):
        acc = BankAccount("Test")
        with self.assertRaises(AttributeError):
            acc.balance = 9999

    def test_repr(self):
        acc = BankAccount("Arjun", 1000.0)
        r = repr(acc)
        self.assertIn("Arjun", r)
        self.assertIn("1000.00", r)


class TestDeposit(unittest.TestCase):

    def setUp(self):
        self.acc = BankAccount("Ananya", initial_balance=1000.0)

    def test_deposit_increases_balance(self):
        self.acc.deposit(500)
        self.assertEqual(self.acc.balance, 1500.0)

    def test_deposit_returns_transaction(self):
        txn = self.acc.deposit(200)
        self.assertIsInstance(txn, Transaction)
        self.assertEqual(txn.txn_type, "deposit")
        self.assertEqual(txn.amount, 200)

    def test_deposit_recorded_in_history(self):
        self.acc.deposit(300)
        self.assertEqual(len(self.acc.history()), 1)

    def test_multiple_deposits(self):
        self.acc.deposit(100)
        self.acc.deposit(200)
        self.acc.deposit(300)
        self.assertEqual(self.acc.balance, 1600.0)
        self.assertEqual(len(self.acc.history()), 3)

    # ── edge cases ────────────────────────────

    def test_zero_deposit_raises(self):
        with self.assertRaises(ValueError):
            self.acc.deposit(0)

    def test_negative_deposit_raises(self):
        with self.assertRaises(ValueError):
            self.acc.deposit(-100)


class TestWithdraw(unittest.TestCase):

    def setUp(self):
        self.acc = BankAccount("Vikram", initial_balance=2000.0)

    def test_withdraw_decreases_balance(self):
        self.acc.withdraw(500)
        self.assertEqual(self.acc.balance, 1500.0)

    def test_withdraw_returns_transaction(self):
        txn = self.acc.withdraw(300)
        self.assertIsInstance(txn, Transaction)
        self.assertEqual(txn.txn_type, "withdrawal")
        self.assertEqual(txn.amount, 300)

    def test_withdraw_recorded_in_history(self):
        self.acc.withdraw(100)
        self.assertEqual(len(self.acc.history()), 1)

    def test_withdraw_exact_balance(self):
        self.acc.withdraw(2000.0)
        self.assertEqual(self.acc.balance, 0.0)

    # ── edge cases ────────────────────────────

    def test_overdraft_raises_overdraft_error(self):
        with self.assertRaises(OverdraftError):
            self.acc.withdraw(9999)

    def test_overdraft_does_not_change_balance(self):
        try:
            self.acc.withdraw(9999)
        except OverdraftError:
            pass
        self.assertEqual(self.acc.balance, 2000.0)  # balance unchanged

    def test_overdraft_not_added_to_history(self):
        try:
            self.acc.withdraw(9999)
        except OverdraftError:
            pass
        self.assertEqual(len(self.acc.history()), 0)  # nothing recorded

    def test_zero_withdrawal_raises(self):
        with self.assertRaises(ValueError):
            self.acc.withdraw(0)

    def test_negative_withdrawal_raises(self):
        with self.assertRaises(ValueError):
            self.acc.withdraw(-50)


class TestHistory(unittest.TestCase):

    def test_empty_history_on_new_account(self):
        acc = BankAccount("New")
        self.assertEqual(acc.history(), [])

    def test_history_returns_copy_not_original(self):
        acc = BankAccount("Copy Test", 500)
        acc.deposit(100)
        h = acc.history()
        h.clear()                         # mutate the copy
        self.assertEqual(len(acc.history()), 1)  # original unaffected

    def test_history_order_preserved(self):
        acc = BankAccount("Order", 1000)
        acc.deposit(100)
        acc.withdraw(50)
        acc.deposit(200)
        h = acc.history()
        self.assertEqual(h[0].txn_type, "deposit")
        self.assertEqual(h[1].txn_type, "withdrawal")
        self.assertEqual(h[2].txn_type, "deposit")


class TestEquality(unittest.TestCase):

    def test_equal_accounts(self):
        a = BankAccount("Sita", 500)
        b = BankAccount("Sita", 500)
        self.assertEqual(a, b)

    def test_different_owner_not_equal(self):
        a = BankAccount("Sita", 500)
        b = BankAccount("Ram", 500)
        self.assertNotEqual(a, b)

    def test_different_balance_not_equal(self):
        a = BankAccount("Sita", 500)
        b = BankAccount("Sita", 600)
        self.assertNotEqual(a, b)

    def test_comparison_with_non_account(self):
        acc = BankAccount("Sita", 500)
        self.assertNotEqual(acc, "not an account")


class TestClassAttributes(unittest.TestCase):

    def test_bank_name_shared(self):
        a = BankAccount("X")
        b = BankAccount("Y")
        self.assertEqual(a.bank_name, b.bank_name)
        self.assertEqual(BankAccount.bank_name, "PyBank")

    def test_total_accounts_increments(self):
        before = BankAccount.total_accounts()
        BankAccount("Counter Test 1")
        BankAccount("Counter Test 2")
        self.assertEqual(BankAccount.total_accounts(), before + 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)