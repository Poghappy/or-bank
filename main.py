#!/usr/bin/env python
"""
ATM Banking System - Command Line Interface
ATM银行系统 - 命令行界面

This is a demonstration CLI for the ATM banking system.
这是ATM银行系统的演示命令行界面。
"""

from atm_banking import Account, ATM


def print_menu():
    """Print the main menu."""
    print("\n" + "=" * 50)
    print("       ATM Banking System | ATM银行系统")
    print("=" * 50)
    print("1. Login (登录)")
    print("2. Register New Account (注册新账户)")
    print("3. Exit (退出)")
    print("=" * 50)


def print_transaction_menu():
    """Print the transaction menu."""
    print("\n" + "-" * 50)
    print("       Transaction Menu | 交易菜单")
    print("-" * 50)
    print("1. Check Balance (查询余额)")
    print("2. Deposit (存款)")
    print("3. Withdraw (取款)")
    print("4. Account Info (账户信息)")
    print("5. Logout (登出)")
    print("-" * 50)


def get_float_input(prompt: str) -> float:
    """Get float input from user with validation."""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def register_account(atm: ATM):
    """Register a new account."""
    print("\n--- Register New Account | 注册新账户 ---")
    
    account_number = input("Enter account number (输入账户号码): ").strip()
    pin = input("Enter 4-digit PIN (输入4位PIN码): ").strip()
    holder_name = input("Enter holder name (输入持有人姓名): ").strip()
    initial_balance = get_float_input("Enter initial balance (输入初始余额): ")
    
    try:
        account = Account(account_number, pin, holder_name, initial_balance)
        if atm.register_account(account):
            print(f"\n✓ Account registered successfully! | 账户注册成功!")
            print(f"  Account Number: {account_number}")
            print(f"  Holder Name: {holder_name}")
            print(f"  Initial Balance: {initial_balance:.2f}")
        else:
            print("\n✗ Account already exists! | 账户已存在!")
    except ValueError as e:
        print(f"\n✗ Registration failed: {e}")


def login(atm: ATM):
    """Login to an account."""
    print("\n--- Login | 登录 ---")
    
    account_number = input("Enter account number (输入账户号码): ").strip()
    pin = input("Enter PIN (输入PIN码): ").strip()
    
    try:
        if atm.authenticate(account_number, pin):
            print("\n✓ Login successful! | 登录成功!")
            handle_transactions(atm)
        else:
            remaining = atm.get_remaining_attempts(account_number)
            print(f"\n✗ Invalid credentials! | 凭证无效!")
            print(f"  Remaining attempts: {remaining}")
    except ValueError as e:
        print(f"\n✗ {e}")


def handle_transactions(atm: ATM):
    """Handle transactions for logged in user."""
    while atm.is_authenticated():
        print_transaction_menu()
        choice = input("Select option (选择选项): ").strip()
        
        if choice == "1":
            # Check balance
            balance = atm.check_balance()
            print(f"\n💰 Current Balance | 当前余额: {balance:.2f}")
            
        elif choice == "2":
            # Deposit
            amount = get_float_input("Enter deposit amount (输入存款金额): ")
            result = atm.deposit(amount)
            if result["success"]:
                print(f"\n✓ {result['message']}")
                print(f"  New Balance: {result['new_balance']:.2f}")
            else:
                print(f"\n✗ {result['message']}")
                
        elif choice == "3":
            # Withdraw
            amount = get_float_input("Enter withdrawal amount (输入取款金额): ")
            result = atm.withdraw(amount)
            if result["success"]:
                print(f"\n✓ {result['message']}")
                print(f"  New Balance: {result['new_balance']:.2f}")
            else:
                print(f"\n✗ {result['message']}")
                
        elif choice == "4":
            # Account info
            info = atm.get_account_info()
            print("\n📋 Account Information | 账户信息:")
            print(f"  Account Number: {info['account_number']}")
            print(f"  Holder Name: {info['holder_name']}")
            print(f"  Balance: {info['balance']:.2f}")
            
        elif choice == "5":
            # Logout
            atm.logout()
            print("\n✓ Logged out successfully! | 登出成功!")
            break
            
        else:
            print("\n✗ Invalid option! | 无效选项!")


def main():
    """Main function to run the ATM system."""
    atm = ATM()
    
    # Pre-register a demo account
    demo_account = Account("1001", "1234", "Demo User", 5000.0)
    atm.register_account(demo_account)
    print("\n📌 Demo account created: 1001 (PIN: 1234)")
    print("   演示账户已创建: 1001 (PIN码: 1234)")
    
    while True:
        print_menu()
        choice = input("Select option (选择选项): ").strip()
        
        if choice == "1":
            login(atm)
        elif choice == "2":
            register_account(atm)
        elif choice == "3":
            print("\n👋 Thank you for using ATM Banking System!")
            print("   感谢使用ATM银行系统!")
            break
        else:
            print("\n✗ Invalid option! | 无效选项!")


if __name__ == "__main__":
    main()
