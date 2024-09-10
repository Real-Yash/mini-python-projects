# Bank Account System

A simple bank account management system built with Python, Tkinter for the GUI, and SQLite for the database.

## Features

- Create a new bank account
- Login to an existing account
- Deposit money
- Withdraw money
- Check account balance
- Retrieve account number using full name and phone number

## Requirements

- Python 3.x
- Tkinter (usually included with Python)
- SQLite3 (usually included with Python)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Real-Yash/mini-python-projects.git
    cd bank-account-system
    ```

2. **Install required packages:**

    Tkinter and SQLite3 are usually included with Python. If not, you can install them using pip:

    ```bash
    pip install tk
    pip install sqlite3
    ```

## Usage

1. **Run the main script:**

    ```bash
    python main.py
    ```

2. **Create a new account:**

    - Click on "Create Account"
    - Enter your full name and phone number
    - Your account number will be generated and displayed

3. **Login to an existing account:**

    - Click on "Login"
    - Enter your full name, account number, and phone number
    - If the credentials are correct, you will be logged in

4. **Deposit money:**

    - After logging in, click on "Deposit"
    - Enter the amount to deposit
    - The amount will be added to your balance

5. **Withdraw money:**

    - After logging in, click on "Withdraw"
    - Enter the amount to withdraw
    - The amount will be deducted from your balance if sufficient funds are available

6. **Check account balance:**

    - After logging in, click on "Balance Inquiry"
    - Your current balance will be displayed

7. **Retrieve account number:**

    - Click on "Login"
    - Click on "Forgot Account Number"
    - Enter your full name and phone number
    - Your account number will be displayed if the details are correct

## Project Structure

```plaintext
bank-account-system/
│
├── main.py                 # Main script to run the application
├── README.md               # Project documentation
└── bank.db                 # SQLite database file (created automatically)
