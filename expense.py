import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

DB_NAME = "expenses.db"

# --------------- DATABASE -------------

def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        type TEXT CHECK(type IN ('income','expense')) NOT NULL,
        category_id INTEGER,
        description TEXT,
        date TEXT NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )
    """)

    conn.commit()
    conn.close()


# ---------------- SERVICES ----------------

def add_category(name):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()


def get_category_id(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM categories WHERE name = ?", (name,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def add_transaction(amount, t_type, category, description=""):
    add_category(category)
    category_id = get_category_id(category)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO transactions (amount, type, category_id, description, date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        amount,
        t_type,
        category_id,
        description,
        datetime.now().strftime("%Y-%m-%d")
    ))
    conn.commit()
    conn.close()


def fetch_transactions():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT t.id, t.amount, t.type, c.name AS category, t.description, t.date
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.id
    """, conn)
    conn.close()
    return df


# -------------------- REPORTS --------------------

def monthly_summary():
    df = fetch_transactions()
    if df.empty:
        print("No data available.")
        return

    df["date"] = pd.to_datetime(df["date"])
    summary = df.groupby([df["date"].dt.to_period("M"), "type"])["amount"].sum()
    print("\nMonthly Summary")
    print(summary)


def category_summary():
    df = fetch_transactions()
    expenses = df[df["type"] == "expense"]

    if expenses.empty:
        print("No expenses found.")
        return

    summary = expenses.groupby("category")["amount"].sum()
    print("\nCategory Summary")
    print(summary)


# -------------------- CHARTS --------------------

def plot_category_pie():
    df = fetch_transactions()
    expenses = df[df["type"] == "expense"]

    if expenses.empty:
        print("No expenses to plot.")
        return

    data = expenses.groupby("category")["amount"].sum()
    data.plot(kind="pie", autopct="%1.1f%%")
    plt.title("Expenses by Category")
    plt.ylabel("")
    plt.show()


def plot_monthly_bar():
    df = fetch_transactions()
    if df.empty:
        print("No data to plot.")
        return

    df["date"] = pd.to_datetime(df["date"])
    monthly = df.groupby(df["date"].dt.to_period("M"))["amount"].sum()
    monthly.plot(kind="bar")
    plt.title("Monthly Cash Flow")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.show()


# -------------------- CLI --------------------

def menu():
    print("""
Expense Tracker System
1. Add Income
2. Add Expense
3. Monthly Summary
4. Category Summary
5. Expense Pie Chart
6. Monthly Bar Chart
0. Exit
""")


def main():
    init_db()

    while True:
        menu()
        choice = input("Choose an option: ")

        if choice == "1":
            amount = float(input("Amount: "))
            category = input("Category: ")
            desc = input("Description: ")
            add_transaction(amount, "income", category, desc)
            print("Income added.")

        elif choice == "2":
            amount = float(input("Amount: "))
            category = input("Category: ")
            desc = input("Description: ")
            add_transaction(amount, "expense", category, desc)
            print("Expense added.")

        elif choice == "3":
            monthly_summary()

        elif choice == "4":
            category_summary()

        elif choice == "5":
            plot_category_pie()

        elif choice == "6":
            plot_monthly_bar()

        elif choice == "0":
            print("Goodbye 👋")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
