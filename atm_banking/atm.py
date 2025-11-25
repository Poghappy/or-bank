"""
ATM module for ATM Banking System
ATM模块 - 自动取款机系统
"""

from typing import Optional
from .account import Account


class ATM:
    """
    ATM class for handling self-service banking operations.
    ATM类 - 处理自助银行操作
    """

    MAX_PIN_ATTEMPTS = 3
    MAX_WITHDRAWAL_LIMIT = 10000.0
    MIN_DEPOSIT_AMOUNT = 1.0

    def __init__(self):
        """
        Initialize the ATM system.
        初始化ATM系统
        """
        self._accounts: dict[str, Account] = {}
        self._current_account: Optional[Account] = None
        self._failed_attempts: dict[str, int] = {}
        self._locked_accounts: set[str] = set()

    def register_account(self, account: Account) -> bool:
        """
        Register a new account with the ATM system.
        在ATM系统中注册新账户

        Args:
            account: Account to register (要注册的账户)

        Returns:
            True if registration was successful, False if account already exists

        Raises:
            ValueError: If account is None or not an Account instance
        """
        if not isinstance(account, Account):
            raise ValueError("Must provide a valid Account instance")

        if account.account_number in self._accounts:
            return False

        self._accounts[account.account_number] = account
        self._failed_attempts[account.account_number] = 0
        return True

    def authenticate(self, account_number: str, pin: str) -> bool:
        """
        Authenticate a user with account number and PIN.
        使用账户号码和PIN码验证用户

        Args:
            account_number: Account number to authenticate (账户号码)
            pin: PIN to verify (PIN码)

        Returns:
            True if authentication was successful, False otherwise

        Raises:
            ValueError: If account is locked due to too many failed attempts
        """
        if account_number in self._locked_accounts:
            raise ValueError("Account is locked due to too many failed PIN attempts")

        if account_number not in self._accounts:
            return False

        account = self._accounts[account_number]

        if account.verify_pin(pin):
            self._current_account = account
            self._failed_attempts[account_number] = 0
            return True
        else:
            self._failed_attempts[account_number] += 1
            if self._failed_attempts[account_number] >= self.MAX_PIN_ATTEMPTS:
                self._locked_accounts.add(account_number)
                raise ValueError("Account locked due to too many failed PIN attempts")
            return False

    def logout(self) -> bool:
        """
        Logout the current user.
        登出当前用户

        Returns:
            True if logout was successful, False if no user was logged in
        """
        if self._current_account is None:
            return False

        self._current_account = None
        return True

    def check_balance(self) -> float:
        """
        Check the balance of the current authenticated account.
        查询当前已验证账户的余额

        Returns:
            Current balance of the account

        Raises:
            ValueError: If no user is authenticated
        """
        if self._current_account is None:
            raise ValueError("No authenticated user. Please login first.")

        return self._current_account.balance

    def deposit(self, amount: float) -> dict:
        """
        Deposit money into the current authenticated account.
        向当前已验证账户存款

        Args:
            amount: Amount to deposit (存款金额)

        Returns:
            Dictionary with transaction result containing:
                - success: bool
                - message: str
                - new_balance: float (if successful)

        Raises:
            ValueError: If no user is authenticated
        """
        if self._current_account is None:
            raise ValueError("No authenticated user. Please login first.")

        if amount < self.MIN_DEPOSIT_AMOUNT:
            return {
                "success": False,
                "message": f"Minimum deposit amount is {self.MIN_DEPOSIT_AMOUNT}"
            }

        try:
            self._current_account.deposit(amount)
            return {
                "success": True,
                "message": f"Successfully deposited {amount:.2f}",
                "new_balance": self._current_account.balance
            }
        except ValueError as e:
            return {
                "success": False,
                "message": str(e)
            }

    def withdraw(self, amount: float) -> dict:
        """
        Withdraw money from the current authenticated account.
        从当前已验证账户取款

        Args:
            amount: Amount to withdraw (取款金额)

        Returns:
            Dictionary with transaction result containing:
                - success: bool
                - message: str
                - new_balance: float (if successful)

        Raises:
            ValueError: If no user is authenticated
        """
        if self._current_account is None:
            raise ValueError("No authenticated user. Please login first.")

        if amount > self.MAX_WITHDRAWAL_LIMIT:
            return {
                "success": False,
                "message": f"Maximum withdrawal limit is {self.MAX_WITHDRAWAL_LIMIT}"
            }

        try:
            self._current_account.withdraw(amount)
            return {
                "success": True,
                "message": f"Successfully withdrew {amount:.2f}",
                "new_balance": self._current_account.balance
            }
        except ValueError as e:
            return {
                "success": False,
                "message": str(e)
            }

    def get_account_info(self) -> dict:
        """
        Get information about the current authenticated account.
        获取当前已验证账户的信息

        Returns:
            Dictionary with account information

        Raises:
            ValueError: If no user is authenticated
        """
        if self._current_account is None:
            raise ValueError("No authenticated user. Please login first.")

        return {
            "account_number": self._current_account.account_number,
            "holder_name": self._current_account.holder_name,
            "balance": self._current_account.balance
        }

    def is_authenticated(self) -> bool:
        """
        Check if a user is currently authenticated.
        检查当前是否有用户已验证

        Returns:
            True if a user is authenticated, False otherwise
        """
        return self._current_account is not None

    def unlock_account(self, account_number: str) -> bool:
        """
        Unlock a locked account (admin function).
        解锁被锁定的账户（管理员功能）

        Args:
            account_number: Account number to unlock (要解锁的账户号码)

        Returns:
            True if account was unlocked, False if account was not locked
        """
        if account_number in self._locked_accounts:
            self._locked_accounts.remove(account_number)
            self._failed_attempts[account_number] = 0
            return True
        return False

    def get_remaining_attempts(self, account_number: str) -> int:
        """
        Get remaining PIN attempts for an account.
        获取账户剩余的PIN尝试次数

        Args:
            account_number: Account number to check (要检查的账户号码)

        Returns:
            Number of remaining attempts, or -1 if account is locked
        """
        if account_number in self._locked_accounts:
            return -1
        if account_number not in self._failed_attempts:
            return self.MAX_PIN_ATTEMPTS
        return self.MAX_PIN_ATTEMPTS - self._failed_attempts[account_number]
