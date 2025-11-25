"""
Unit tests for Account class
账户类单元测试
"""

import unittest
import sys
import os

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from atm_banking.account import Account


class TestAccountCreation(unittest.TestCase):
    """Test cases for Account creation and initialization."""

    def test_create_account_with_valid_data(self):
        """Test creating an account with valid data."""
        account = Account("1234567890", "1234", "John Doe", 1000.0)
        self.assertEqual(account.account_number, "1234567890")
        self.assertEqual(account.holder_name, "John Doe")
        self.assertEqual(account.balance, 1000.0)

    def test_create_account_with_default_balance(self):
        """Test creating an account with default balance."""
        account = Account("1234567890", "1234", "John Doe")
        self.assertEqual(account.balance, 0.0)

    def test_create_account_with_integer_balance(self):
        """Test creating an account with integer initial balance."""
        account = Account("1234567890", "1234", "John Doe", 500)
        self.assertEqual(account.balance, 500.0)

    def test_create_account_with_empty_account_number(self):
        """Test that creating an account with empty account number raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Account("", "1234", "John Doe")
        self.assertIn("Account number must be a non-empty string", str(context.exception))

    def test_create_account_with_invalid_pin_length(self):
        """Test that creating an account with invalid PIN length raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Account("1234567890", "123", "John Doe")
        self.assertIn("PIN must be a 4-digit string", str(context.exception))

    def test_create_account_with_non_numeric_pin(self):
        """Test that creating an account with non-numeric PIN raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Account("1234567890", "abcd", "John Doe")
        self.assertIn("PIN must be a 4-digit string", str(context.exception))

    def test_create_account_with_empty_holder_name(self):
        """Test that creating an account with empty holder name raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Account("1234567890", "1234", "")
        self.assertIn("Holder name must be a non-empty string", str(context.exception))

    def test_create_account_with_negative_balance(self):
        """Test that creating an account with negative balance raises ValueError."""
        with self.assertRaises(ValueError) as context:
            Account("1234567890", "1234", "John Doe", -100.0)
        self.assertIn("Initial balance must be a non-negative number", str(context.exception))


class TestAccountPinVerification(unittest.TestCase):
    """Test cases for Account PIN verification."""

    def setUp(self):
        """Set up test account."""
        self.account = Account("1234567890", "1234", "John Doe", 1000.0)

    def test_verify_correct_pin(self):
        """Test verifying correct PIN."""
        self.assertTrue(self.account.verify_pin("1234"))

    def test_verify_incorrect_pin(self):
        """Test verifying incorrect PIN."""
        self.assertFalse(self.account.verify_pin("9999"))

    def test_verify_empty_pin(self):
        """Test verifying empty PIN."""
        self.assertFalse(self.account.verify_pin(""))


class TestAccountDeposit(unittest.TestCase):
    """Test cases for Account deposit functionality."""

    def setUp(self):
        """Set up test account."""
        self.account = Account("1234567890", "1234", "John Doe", 1000.0)

    def test_deposit_positive_amount(self):
        """Test depositing a positive amount."""
        result = self.account.deposit(500.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 1500.0)

    def test_deposit_integer_amount(self):
        """Test depositing an integer amount."""
        result = self.account.deposit(500)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 1500.0)

    def test_deposit_zero_amount(self):
        """Test that depositing zero raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.deposit(0)
        self.assertIn("Deposit amount must be a positive number", str(context.exception))

    def test_deposit_negative_amount(self):
        """Test that depositing negative amount raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.deposit(-100.0)
        self.assertIn("Deposit amount must be a positive number", str(context.exception))


class TestAccountWithdrawal(unittest.TestCase):
    """Test cases for Account withdrawal functionality."""

    def setUp(self):
        """Set up test account."""
        self.account = Account("1234567890", "1234", "John Doe", 1000.0)

    def test_withdraw_valid_amount(self):
        """Test withdrawing a valid amount."""
        result = self.account.withdraw(500.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 500.0)

    def test_withdraw_entire_balance(self):
        """Test withdrawing entire balance."""
        result = self.account.withdraw(1000.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 0.0)

    def test_withdraw_more_than_balance(self):
        """Test that withdrawing more than balance raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(1500.0)
        self.assertIn("Insufficient balance", str(context.exception))

    def test_withdraw_zero_amount(self):
        """Test that withdrawing zero raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(0)
        self.assertIn("Withdrawal amount must be a positive number", str(context.exception))

    def test_withdraw_negative_amount(self):
        """Test that withdrawing negative amount raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(-100.0)
        self.assertIn("Withdrawal amount must be a positive number", str(context.exception))


class TestAccountRepresentation(unittest.TestCase):
    """Test cases for Account string representation."""

    def setUp(self):
        """Set up test account."""
        self.account = Account("1234567890", "1234", "John Doe", 1000.0)

    def test_str_representation(self):
        """Test string representation of account."""
        result = str(self.account)
        self.assertIn("1234567890", result)
        self.assertIn("John Doe", result)
        self.assertIn("1000.00", result)

    def test_repr_representation(self):
        """Test repr representation of account."""
        result = repr(self.account)
        self.assertIn("1234567890", result)
        self.assertIn("John Doe", result)


if __name__ == '__main__':
    unittest.main()
