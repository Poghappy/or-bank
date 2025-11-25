# Exp-1 ATM & BANKING SYSTEM

## Python Self-Service Deposit and Withdrawal Verification Project
## Python 自助存取验证项目

---

## AIM:
To design and implement a Python-based ATM banking system that provides self-service deposit and withdrawal functionality with PIN verification and account management features.

设计并实现一个基于Python的ATM银行系统，提供自助存取款功能，包含PIN验证和账户管理功能。

---

## SRS (Software Requirements Specification):

### Functional Requirements:
1. **Account Management (账户管理)**
   - Create new bank accounts with unique account numbers
   - Store account holder information
   - Maintain account balance

2. **Authentication (身份验证)**
   - PIN-based authentication (4-digit PIN)
   - Account lockout after 3 failed attempts
   - Account unlock functionality (admin)

3. **Deposit Operations (存款操作)**
   - Accept deposits with minimum amount validation
   - Update account balance after successful deposit
   - Provide transaction confirmation

4. **Withdrawal Operations (取款操作)**
   - Process withdrawals with balance validation
   - Maximum withdrawal limit enforcement
   - Update account balance after successful withdrawal

5. **Balance Inquiry (余额查询)**
   - Display current account balance
   - Show account holder information

### Non-Functional Requirements:
- Input validation for all operations
- Error handling and appropriate messages
- Bilingual support (English/Chinese)

---

## Project Structure:

```
or-bank/
├── atm_banking/
│   ├── __init__.py      # Package initialization
│   ├── account.py       # Account class implementation
│   └── atm.py           # ATM class implementation
├── tests/
│   ├── __init__.py      # Tests initialization
│   ├── test_account.py  # Account unit tests
│   └── test_atm.py      # ATM unit tests
├── main.py              # CLI demonstration
└── README.md            # Documentation
```

---

## Usage:

### Running the CLI Demo:
```bash
python main.py
```

### Using as a Module:
```python
from atm_banking import Account, ATM

# Create an ATM instance
atm = ATM()

# Register an account
account = Account("1001", "1234", "John Doe", 1000.0)
atm.register_account(account)

# Authenticate
atm.authenticate("1001", "1234")

# Check balance
balance = atm.check_balance()

# Deposit
result = atm.deposit(500.0)

# Withdraw
result = atm.withdraw(200.0)

# Logout
atm.logout()
```

### Running Tests:
```bash
python -m unittest discover -v tests/
```

---

## DIAGRAMS:

### 1. Use Case Diagram (用例图)
```
                    +------------------------+
                    |    ATM Banking System  |
                    +------------------------+
                              |
          +-------------------+-------------------+
          |                   |                   |
    +----------+        +-----------+       +-----------+
    |  Login   |        |  Deposit  |       | Withdraw  |
    +----------+        +-----------+       +-----------+
          |                   |                   |
          |             +-----------+             |
          +-------------|  Balance  |-------------+
                        |  Inquiry  |
                        +-----------+
                              |
                        +-----------+
                        |  Logout   |
                        +-----------+
```

### 2. Class Diagram (类图)
```
+---------------------------+       +---------------------------+
|         Account           |       |           ATM             |
+---------------------------+       +---------------------------+
| - _account_number: str    |       | - _accounts: dict         |
| - _pin: str               |       | - _current_account: Account|
| - _holder_name: str       |       | - _failed_attempts: dict  |
| - _balance: float         |       | - _locked_accounts: set   |
+---------------------------+       +---------------------------+
| + account_number: str     |       | + MAX_PIN_ATTEMPTS: int   |
| + holder_name: str        |       | + MAX_WITHDRAWAL_LIMIT: float|
| + balance: float          |       | + MIN_DEPOSIT_AMOUNT: float|
+---------------------------+       +---------------------------+
| + verify_pin(pin): bool   |       | + register_account(): bool|
| + deposit(amount): bool   |       | + authenticate(): bool    |
| + withdraw(amount): bool  |       | + logout(): bool          |
+---------------------------+       | + check_balance(): float  |
                                    | + deposit(): dict         |
                                    | + withdraw(): dict        |
                                    | + get_account_info(): dict|
                                    +---------------------------+
```

### 3. Sequence Diagram - Deposit (存款顺序图)
```
User        ATM         Account
 |           |             |
 |--login--->|             |
 |           |--verify---->|
 |           |<--success---|
 |<-success--|             |
 |           |             |
 |--deposit->|             |
 |           |--deposit--->|
 |           |<--balance---|
 |<-receipt--|             |
```

### 4. Sequence Diagram - Withdraw (取款顺序图)
```
User        ATM         Account
 |           |             |
 |--login--->|             |
 |           |--verify---->|
 |           |<--success---|
 |<-success--|             |
 |           |             |
 |--withdraw>|             |
 |           |--check bal->|
 |           |<--balance---|
 |           |--withdraw-->|
 |           |<--success---|
 |<-cash-----|             |
```

### 5. Activity Diagram - ATM Operations (ATM操作活动图)
```
    [Start]
       |
       v
  [Main Menu]
       |
   /       \
  v         v
[Login]  [Register]
  |           |
  v           v
[Enter PIN]  [Create Account]
  |           |
  |     +-----+
  v     |
[Verify]|
  |     |
  v     v
[Transaction Menu]
  |
  +->[Balance]
  |
  +->[Deposit]
  |
  +->[Withdraw]
  |
  +->[Logout]->[End]
```

### 6. State Diagram - Account States (账户状态图)
```
+----------+   create   +----------+   3 failed   +----------+
|  (new)   |----------->|  Active  |------------->|  Locked  |
+----------+            +----------+    attempts   +----------+
                             ^                          |
                             |        unlock            |
                             +--------------------------+
```

---

## RESULT:
Successfully implemented a Python ATM Banking System with the following features:

1. ✅ Account creation with PIN verification
2. ✅ Secure authentication with account lockout
3. ✅ Deposit functionality with validation
4. ✅ Withdrawal functionality with balance check
5. ✅ Balance inquiry
6. ✅ Comprehensive unit tests (50 tests passing)
7. ✅ Bilingual support (English/Chinese)

成功实现了Python ATM银行系统，包含以下功能：
1. ✅ 带PIN验证的账户创建
2. ✅ 带账户锁定的安全验证
3. ✅ 带验证的存款功能
4. ✅ 带余额检查的取款功能
5. ✅ 余额查询
6. ✅ 全面的单元测试（50个测试通过）
7. ✅ 双语支持（英文/中文）
