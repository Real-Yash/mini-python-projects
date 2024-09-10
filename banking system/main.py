import tkinter as tk
# https://www.geeksforgeeks.org/python-tkinter-tutorial/
# https://www.tutorialspoint.com/python/python_gui_programming.htm
from tkinter import messagebox
import random
import sqlite3
# https://docs.python.org/3/library/sqlite3.html
# https://www.sqlitetutorial.net/sqlite-python/creating-database/
from queue import Queue

class BankAccount:
    def __init__(self, full_name, phone_number, account_number=None, balance=0):
        self.full_name = full_name
        self.phone_number = phone_number
        self.account_number = account_number if account_number else random.randint(1000, 9999)
        self.balance = balance
        self.transactions = Queue()

    def deposit(self, amount):
        amount = self._sanitize_amount(amount)
        if amount > 0:
            self.transactions.put(('deposit', amount))
            self.balance += amount
            self.update_balance_in_db()
            return f"Deposited: rs.{amount}"
        else:
            return "Deposit amount must be positive."

    def withdraw(self, amount):
        amount = self._sanitize_amount(amount)
        if 0 < amount <= self.balance:
            self.transactions.put(('withdraw', amount))
            self.balance -= amount
            self.update_balance_in_db()
            return f"Withdrew: rs.{amount}"
        else:
            return "Insufficient funds or invalid amount."

    def balance_inquiry(self):
        return f"Current Balance: rs.{self.balance}"

    def update_balance_in_db(self):
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (self.balance, self.account_number))
        conn.commit()
        conn.close()

    def _sanitize_amount(self, amount):
        if isinstance(amount, str):
            amount = amount.replace(',', '')
        return float(amount)

def create_account(full_name, phone_number):
    account = BankAccount(full_name, phone_number)
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO accounts (full_name, phone_number, account_number, balance) VALUES (?, ?, ?, ?)",
                   (account.full_name, account.phone_number, account.account_number, account.balance))
    conn.commit()
    conn.close()
    return account

def login(full_name, account_number):
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE full_name = ? AND account_number = ?", (full_name, account_number))
    row = cursor.fetchone()
    conn.close()
    if row:
        return BankAccount(row[0], row[1], row[2], row[3])
    else:
        return None

def retrieve_account_number(full_name, phone_number):
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute("SELECT account_number FROM accounts WHERE full_name = ? AND phone_number = ?", (full_name, phone_number))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    else:
        return None

def main():
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts
                      (full_name TEXT, phone_number TEXT, account_number INTEGER, balance REAL)''')
    conn.commit()
    conn.close()

    root = tk.Tk()
    root.title("Bank Account System")
    root.geometry("480x270")  # Set the window size

    def create_account_ui():
        def submit():
            full_name = entry_full_name.get()
            phone_number = entry_phone_number.get()
            account = create_account(full_name, phone_number)
            messagebox.showinfo("Account Created", f"Account created successfully! Your account number is {account.account_number}")
            create_account_window.destroy()

        create_account_window = tk.Toplevel(root)
        create_account_window.title("Create Account")
        create_account_window.geometry("480x270")  # Set the window size

        for widget in create_account_window.winfo_children():
            widget.grid_configure(padx=10, pady=10)

        tk.Label(create_account_window, text="Full Name", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
        entry_full_name = tk.Entry(create_account_window, font=("Arial", 12))
        entry_full_name.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(create_account_window, text="Phone Number", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
        entry_phone_number = tk.Entry(create_account_window, font=("Arial", 12))
        entry_phone_number.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(create_account_window, text="Submit", command=submit, font=("Arial", 12)).grid(row=2, columnspan=2, pady=10)

    def login_ui():
        def submit():
            full_name = entry_full_name.get()
            account_number = entry_account_number.get()
            account = login(full_name, account_number)
            if account:
                account_menu_ui(account)
                login_window.destroy()
            else:
                messagebox.showerror("Login Failed", "Invalid login credentials.")

        def forgot_account_number():
            full_name = entry_full_name.get()
            phone_number = entry_phone_number.get()
            account_number = retrieve_account_number(full_name, phone_number)
            if account_number:
                messagebox.showinfo("Account Number Retrieved", f"Your account number is {account_number}")
            else:
                messagebox.showerror("Error", "No account found with the provided details.")

        login_window = tk.Toplevel(root)
        login_window.title("Login")
        login_window.geometry("480x270")  # Set the window size

        for widget in login_window.winfo_children():
            widget.grid_configure(padx=10, pady=10)

        tk.Label(login_window, text="Full Name", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
        entry_full_name = tk.Entry(login_window, font=("Arial", 12))
        entry_full_name.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(login_window, text="Account Number", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
        entry_account_number = tk.Entry(login_window, font=("Arial", 12))
        entry_account_number.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(login_window, text="Phone Number", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
        entry_phone_number = tk.Entry(login_window, font=("Arial", 12))
        entry_phone_number.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(login_window, text="Submit", command=submit, font=("Arial", 12)).grid(row=3, columnspan=2, pady=10)
        tk.Button(login_window, text="Forgot Account Number", command=forgot_account_number, font=("Arial", 12)).grid(row=4, columnspan=2, pady=10)

    def account_menu_ui(account):
        def deposit_ui():
            def submit():
                amount = entry_amount.get()
                message = account.deposit(amount)
                messagebox.showinfo("Deposit", message)
                deposit_window.destroy()

            deposit_window = tk.Toplevel(root)
            deposit_window.title("Deposit")
            deposit_window.geometry("480x270")  # Set the window size

            for widget in deposit_window.winfo_children():
                widget.grid_configure(padx=10, pady=10)

            tk.Label(deposit_window, text="Amount", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
            entry_amount = tk.Entry(deposit_window, font=("Arial", 12))
            entry_amount.grid(row=0, column=1, padx=10, pady=10)

            tk.Button(deposit_window, text="Submit", command=submit, font=("Arial", 12)).grid(row=1, columnspan=2, pady=10)

        def withdraw_ui():
            def submit():
                amount = entry_amount.get()
                message = account.withdraw(amount)
                messagebox.showinfo("Withdraw", message)
                withdraw_window.destroy()

            withdraw_window = tk.Toplevel(root)
            withdraw_window.title("Withdraw")
            withdraw_window.geometry("480x270")  # Set the window size

            for widget in withdraw_window.winfo_children():
                widget.grid_configure(padx=10, pady=10)

            tk.Label(withdraw_window, text="Amount", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
            entry_amount = tk.Entry(withdraw_window, font=("Arial", 12))
            entry_amount.grid(row=0, column=1, padx=10, pady=10)

            tk.Button(withdraw_window, text="Submit", command=submit, font=("Arial", 12)).grid(row=1, columnspan=2, pady=10)

        def balance_inquiry_ui():
            message = account.balance_inquiry()
            messagebox.showinfo("Balance Inquiry", message)

        account_menu_window = tk.Toplevel(root)
        account_menu_window.title("Account Menu")
        account_menu_window.geometry("480x270")  # Set the window size

        for widget in account_menu_window.winfo_children():
            widget.grid_configure(padx=10, pady=10)

        tk.Button(account_menu_window, text="Deposit", command=deposit_ui, font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(account_menu_window, text="Withdraw", command=withdraw_ui, font=("Arial", 12)).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(account_menu_window, text="Balance Inquiry", command=balance_inquiry_ui, font=("Arial", 12)).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(account_menu_window, text="Logout", command=account_menu_window.destroy, font=("Arial", 12)).grid(row=2, column=0, columnspan=2, pady=10)

    tk.Button(root, text="Create Account", command=create_account_ui, font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="Login", command=login_ui, font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit, font=("Arial", 14)).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()