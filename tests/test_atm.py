"""
Unit tests for ATM class
ATM类单元测试
"""

import unittest
import sys
import os

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from atm_banking.account import Account
from atm_banking.atm import ATM


class TestATMRegistration(unittest.TestCase):
    """Test cases for ATM account registration."""

    def setUp(self):
        """Set up test ATM and accounts."""
        self.atm = ATM()
        self.account = Account("1234567890", "1234", "John Doe", 1000.0)

    def test_register_account(self):
        """Test registering a new account."""
        result = self.atm.register_account(self.account)
        self.assertTrue(result)

    def test_register_duplicate_account(self):
        """Test that registering duplicate account returns False."""
        self.atm.register_account(self.account)
        result = self.atm.register_account(self.account)
        self.assertFalse(result)

    def test_register_invalid_account(self):
        """Test that registering invalid account raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.atm.register_account("not an account")
        self.assertIn("Must provide a valid Account instance", str(context.exception))


class TestATMAuthentication(unittest.TestCase):
    """Test cases for ATM authentication."""

    def setUp(self):
        """Set up test ATM and accounts."""
        self.atm = ATM()
        self.account = Account("1234567890", "1234", "John Doe", 1000.0)
        self.atm.register_account(self.account)

    def test_authenticate_with_valid_credentials(self):
        """Test authentication with valid credentials."""
        result = self.atm.authenticate("1234567890", "1234")
        self.assertTrue(result)
        self.assertTrue(self.atm.is_authenticated())

    def test_authenticate_with_wrong_pin(self):
        """Test authentication with wrong PIN."""
        result = self.atm.authenticate("1234567890", "9999")
        self.assertFalse(result)
        self.assertFalse(self.atm.is_authenticated())

    def test_authenticate_with_nonexistent_account(self):
        """Test authentication with nonexistent account."""
        result = self.atm.authenticate("9999999999", "1234")
        self.assertFalse(result)

    def test_account_lockout_after_max_attempts(self):
        """Test that account gets locked after max failed attempts."""
        self.atm.authenticate("1234567890", "9999")  # Attempt 1
        self.atm.authenticate("1234567890", "9999")  # Attempt 2
        
        with self.assertRaises(ValueError) as context:
            self.atm.authenticate("1234567890", "9999")  # Attempt 3 - should lock
        self.assertIn("locked", str(context.exception).lower())

    def test_authenticate_locked_account(self):
        """Test that authenticating locked account raises ValueError."""
        # Lock the account
        self.atm.authenticate("1234567890", "9999")
        self.atm.authenticate("1234567890", "9999")
        try:
            self.atm.authenticate("1234567890", "9999")
        except ValueError:
            pass
        
        # Try to authenticate again
        with self.assertRaises(ValueError) as context:
            self.atm.authenticate("1234567890", "1234")
        self.assertIn("locked", str(context.exception).lower())

    def test_successful_auth_resets_failed_attempts(self):
        """Test that successful authentication resets failed attempts counter."""
        self.atm.authenticate("1234567890", "9999")  # Failed attempt
        self.assertEqual(self.atm.get_remaining_attempts("1234567890"), 2)
        
        self.atm.authenticate("1234567890", "1234")  # Successful
        self.assertEqual(self.atm.get_remaining_attempts("1234567890"), 3)


class TestATMLogout(unittest.TestCase):
    """Test cases for ATM logout."""

    def setUp(self):
        """Set up test ATM and accounts."""
        self.atm = ATM()
        self.account = Account("1234567890", "1234", "John Doe", 1000.0)
        self.atm.register_account(self.account)

    def test_logout_authenticated_user(self):
        """Test logging out an authenticated user."""
        self.atm.authenticate("1234567890", "1234")
        result = self.atm.logout()
        self.assertTrue(result)
        self.assertFalse(self.atm.is_authenticated())

    def test_logout_without_authentication(self):
        """Test logout without authentication returns False."""
        result = self.atm.logout()
        self.assertFalse(result)


class TestATMCheckBalance(unittest.TestCase):
    """Test cases for ATM balance checking."""

    def setUp(self):
        """Set up test ATM and accounts."""
        self.atm = ATM()
        self.account = Account("1234567890", "1234", "John Doe", 1000.0)
        self.atm.register_account(self.account)

    def test_check_balance_authenticated(self):
        """Test checking balance when authenticated."""
        self.atm.authenticate("1234567890", "1234")
        balance = self.atm.check_balance()
        self.assertEqual(balance, 1000.0)

    def test_check_balance_unauthenticated(self):
        """Test that checking balance without authentication raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.atm.check_balance()
        self.assertIn("No authenticated user", str(context.exception))


class TestATMDeposit(unittest.TestCase):
    """Test cases for ATM deposit functionality."""

    def setUp(self):
        """Set up test ATM and accounts."""
        self.atm = ATM()
        self.account = Account("1234567890", "1234", "John Doe", 1000.0)
        self.atm.register_account(self.account)
        self.atm.authenticate("1234567890", "1234")

    def test_deposit_valid_amount(self):
        """Test depositing a valid amount."""
        result = self.atm.deposit(500.0)
        self.assertTrue(result["success"])
        self.assertEqual(result["new_balance"], 1500.0)
        self.assertIn("Successfully deposited", result["message"])

    def test_deposit_below_minimum(self):
        """Test that depositing below minimum returns failure."""
        result = self.atm.deposit(0.5)
        self.assertFalse(result["success"])
        self.assertIn("Minimum deposit amount", result["message"])

    def test_deposit_unauthenticated(self):
        """Test that deposit without authentication raises ValueError."""
        self.atm.logout()
        with self.assertRaises(ValueError) as context:
            self.atm.deposit(100.0)
        self.assertIn("No authenticated user", str(context.exception))


class TestATMWithdrawal(unittest.TestCase):
    """Test cases for ATM withdrawal functionality."""

    def setUp(self):
        """Set up test ATM and accounts."""
        self.atm = ATM()
        self.account = Account("1234567890", "1234", "John Doe", 1000.0)
        self.atm.register_account(self.account)
        self.atm.authenticate("1234567890", "1234")

    def test_withdraw_valid_amount(self):
        """Test withdrawing a valid amount."""
        result = self.atm.withdraw(500.0)
        self.assertTrue(result["success"])
        self.assertEqual(result["new_balance"], 500.0)
        self.assertIn("Successfully withdrew", result["message"])

    def test_withdraw_exceeds_balance(self):
        """Test that withdrawing more than balance returns failure."""
        result = self.atm.withdraw(1500.0)
        self.assertFalse(result["success"])
        self.assertIn("Insufficient balance", result["message"])

    def test_withdraw_exceeds_limit(self):
        """Test that withdrawing more than limit returns failure."""
        # First deposit enough
        self.atm.deposit(20000.0)
        result = self.atm.withdraw(15000.0)
        self.assertFalse(result["success"])
        self.assertIn("Maximum withdrawal limit", result["message"])

    def test_withdraw_unauthenticated(self):
        """Test that withdrawal without authentication raises ValueError."""
        self.atm.logout()
        with self.assertRaises(ValueError) as context:
            self.atm.withdraw(100.0)
        self.assertIn("No authenticated user", str(context.exception))


class TestATMAccountInfo(unittest.TestCase):
    """Test cases for ATM account info."""

    def setUp(self):
        """Set up test ATM and accounts."""
        self.atm = ATM()
        self.account = Account("1234567890", "1234", "John Doe", 1000.0)
        self.atm.register_account(self.account)

    def test_get_account_info_authenticated(self):
        """Test getting account info when authenticated."""
        self.atm.authenticate("1234567890", "1234")
        info = self.atm.get_account_info()
        self.assertEqual(info["account_number"], "1234567890")
        self.assertEqual(info["holder_name"], "John Doe")
        self.assertEqual(info["balance"], 1000.0)

    def test_get_account_info_unauthenticated(self):
        """Test that getting account info without authentication raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.atm.get_account_info()
        self.assertIn("No authenticated user", str(context.exception))


class TestATMAccountUnlock(unittest.TestCase):
    """Test cases for ATM account unlock functionality."""

    def setUp(self):
        """Set up test ATM and accounts."""
        self.atm = ATM()
        self.account = Account("1234567890", "1234", "John Doe", 1000.0)
        self.atm.register_account(self.account)

    def test_unlock_locked_account(self):
        """Test unlocking a locked account."""
        # Lock the account
        self.atm.authenticate("1234567890", "9999")
        self.atm.authenticate("1234567890", "9999")
        try:
            self.atm.authenticate("1234567890", "9999")
        except ValueError:
            pass
        
        # Unlock the account
        result = self.atm.unlock_account("1234567890")
        self.assertTrue(result)
        
        # Should be able to authenticate now
        auth_result = self.atm.authenticate("1234567890", "1234")
        self.assertTrue(auth_result)

    def test_unlock_non_locked_account(self):
        """Test unlocking a non-locked account returns False."""
        result = self.atm.unlock_account("1234567890")
        self.assertFalse(result)


class TestATMRemainingAttempts(unittest.TestCase):
    """Test cases for ATM remaining attempts functionality."""

    def setUp(self):
        """Set up test ATM and accounts."""
        self.atm = ATM()
        self.account = Account("1234567890", "1234", "John Doe", 1000.0)
        self.atm.register_account(self.account)

    def test_get_remaining_attempts_new_account(self):
        """Test getting remaining attempts for new account."""
        attempts = self.atm.get_remaining_attempts("1234567890")
        self.assertEqual(attempts, 3)

    def test_get_remaining_attempts_after_failed_attempt(self):
        """Test getting remaining attempts after failed attempt."""
        self.atm.authenticate("1234567890", "9999")
        attempts = self.atm.get_remaining_attempts("1234567890")
        self.assertEqual(attempts, 2)

    def test_get_remaining_attempts_locked_account(self):
        """Test getting remaining attempts for locked account."""
        self.atm.authenticate("1234567890", "9999")
        self.atm.authenticate("1234567890", "9999")
        try:
            self.atm.authenticate("1234567890", "9999")
        except ValueError:
            pass
        
        attempts = self.atm.get_remaining_attempts("1234567890")
        self.assertEqual(attempts, -1)

    def test_get_remaining_attempts_unknown_account(self):
        """Test getting remaining attempts for unknown account."""
        attempts = self.atm.get_remaining_attempts("9999999999")
        self.assertEqual(attempts, 3)


if __name__ == '__main__':
    unittest.main()
