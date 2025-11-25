"""
Account module for ATM Banking System
账户模块 - 用于ATM银行系统
"""


class Account:
    """
    Account class representing a bank account.
    银行账户类
    """

    def __init__(self, account_number: str, pin: str, holder_name: str, initial_balance: float = 0.0):
        """
        Initialize a new bank account.
        初始化新银行账户

        Args:
            account_number: Unique account identifier (账户号码)
            pin: 4-digit PIN for authentication (4位PIN码用于验证)
            holder_name: Name of the account holder (账户持有人姓名)
            initial_balance: Initial balance (default 0.0) (初始余额)

        Raises:
            ValueError: If account_number, pin, or holder_name is invalid
        """
        if not account_number or not isinstance(account_number, str):
            raise ValueError("Account number must be a non-empty string")
        if not pin or not isinstance(pin, str) or len(pin) != 4 or not pin.isdigit():
            raise ValueError("PIN must be a 4-digit string")
        if not holder_name or not isinstance(holder_name, str):
            raise ValueError("Holder name must be a non-empty string")
        if not isinstance(initial_balance, (int, float)) or initial_balance < 0:
            raise ValueError("Initial balance must be a non-negative number")

        self._account_number = account_number
        self._pin = pin
        self._holder_name = holder_name
        self._balance = float(initial_balance)

    @property
    def account_number(self) -> str:
        """Get the account number."""
        return self._account_number

    @property
    def holder_name(self) -> str:
        """Get the account holder's name."""
        return self._holder_name

    @property
    def balance(self) -> float:
        """Get the current balance."""
        return self._balance

    def verify_pin(self, pin: str) -> bool:
        """
        Verify if the provided PIN matches the account PIN.
        验证提供的PIN码是否与账户PIN码匹配

        Args:
            pin: PIN to verify (待验证的PIN码)

        Returns:
            True if PIN matches, False otherwise
        """
        return self._pin == pin

    def deposit(self, amount: float) -> bool:
        """
        Deposit money into the account.
        存款到账户

        Args:
            amount: Amount to deposit (must be positive) (存款金额，必须为正数)

        Returns:
            True if deposit was successful, False otherwise

        Raises:
            ValueError: If amount is not a positive number
        """
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Deposit amount must be a positive number")

        self._balance += float(amount)
        return True

    def withdraw(self, amount: float) -> bool:
        """
        Withdraw money from the account.
        从账户取款

        Args:
            amount: Amount to withdraw (must be positive and <= balance)
                   (取款金额，必须为正数且不超过余额)

        Returns:
            True if withdrawal was successful, False otherwise

        Raises:
            ValueError: If amount is not a positive number or exceeds balance
        """
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Withdrawal amount must be a positive number")

        if amount > self._balance:
            raise ValueError("Insufficient balance for withdrawal")

        self._balance -= float(amount)
        return True

    def __str__(self) -> str:
        """Return string representation of the account."""
        return f"Account({self._account_number}, {self._holder_name}, Balance: {self._balance:.2f})"

    def __repr__(self) -> str:
        """Return detailed representation of the account."""
        return f"Account(account_number='{self._account_number}', holder_name='{self._holder_name}', balance={self._balance})"
