import random
import sqlite3
from queue import Queue

class BankAccount:
    def __init__(self, full_name, phone_number, account_number=None, balance=0):
        self.full_name = full_name
        self.phone_number = phone_number
        # Generate a random account number if not provided
        self.account_number = account_number if account_number else random.randint(1000, 9999)
        self.balance = balance
        # Use a queue to manage transactions
        self.transactions = Queue()

    def deposit(self, amount):
        amount = self._sanitize_amount(amount)
        if amount > 0:
            self.transactions.put(('deposit', amount))
            self.balance += amount
            self.update_balance_in_db()
            print(f"Deposited: rs.{amount}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        amount = self._sanitize_amount(amount)
        if 0 < amount <= self.balance:
            self.transactions.put(('withdraw', amount))
            self.balance -= amount
            self.update_balance_in_db()
            print(f"Withdrew: rs.{amount}")
        else:
            print("Insufficient funds or invalid amount.")

    def balance_inquiry(self):
        print(f"Current Balance: rs.{self.balance}")

    def process_transactions(self):
        while not self.transactions.empty():
            transaction = self.transactions.get()
            print(f"Processed transaction: {transaction[0]} of rs.{transaction[1]}")

    def update_balance_in_db(self):
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        # Update the balance in the database
        cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (self.balance, self.account_number))
        conn.commit()
        conn.close()

    def _sanitize_amount(self, amount):
        # Remove commas from the amount string and convert to float
        if isinstance(amount, str):
            amount = amount.replace(',', '')
        return float(amount)

def create_account():
    full_name = input("Enter your full name: ")
    phone_number = input("Enter your phone number: ")
    account = BankAccount(full_name, phone_number)
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    # Insert new account details into the database
    cursor.execute("INSERT INTO accounts (full_name, phone_number, account_number, balance) VALUES (?, ?, ?, ?)",
                   (account.full_name, account.phone_number, account.account_number, account.balance))
    conn.commit()
    conn.close()
    print(f"Account created successfully! Your account number is {account.account_number}")
    return account

def login():
    full_name = input("Enter your full name: ")
    account_number = int(input("Enter your account number: "))
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    # Fetch account details from the database
    cursor.execute("SELECT * FROM accounts WHERE full_name = ? AND account_number = ?", (full_name, account_number))
    row = cursor.fetchone()
    conn.close()
    if row:
        return BankAccount(row[0], row[1], row[2], row[3])
    else:
        print("Invalid login credentials.")
        forget_account_number_option = input("Forgot your account number? (yes/no): ")
        if forget_account_number_option.lower() == 'yes':
            forget_account_number()
        return None

def forget_account_number():
    full_name = input("Enter your full name: ")
    phone_number = input("Enter your phone number: ")
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    # Retrieve account number based on full name and phone number
    cursor.execute("SELECT account_number FROM accounts WHERE full_name = ? AND phone_number = ?", (full_name, phone_number))
    row = cursor.fetchone()
    conn.close()
    if row:
        print(f"Your account number is {row[0]}")
    else:
        print("No account found with the provided details.")

def main():
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    # Create accounts table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts
                      (full_name TEXT, phone_number TEXT, account_number INTEGER, balance REAL)''')
    conn.commit()
    conn.close()

    while True:
        print("\nBank Account Menu:")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            create_account()
        elif choice == '2':
            account = login()
            if account:
                while True:
                    print("\nAccount Menu:")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Balance Inquiry")
                    print("4. Logout")
                    sub_choice = input("Enter your choice: ")

                    if sub_choice == '1':
                        amount = input("Enter amount to deposit: ")
                        account.deposit(amount)
                    elif sub_choice == '2':
                        amount = input("Enter amount to withdraw: ")
                        account.withdraw(amount)
                    elif sub_choice == '3':
                        account.balance_inquiry()
                    elif sub_choice == '4':
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()