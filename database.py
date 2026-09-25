"""
database.py
------------
All SQLite database access lives here. The database and table are
created automatically the first time the app runs, so there is no
manual setup step.
"""

import sqlite3
import os
from datetime import datetime

DB_FOLDER = "data"
DB_PATH = os.path.join(DB_FOLDER, "finance.db")


def get_connection():
    """Open (and if needed, create the folder for) the SQLite connection."""
    os.makedirs(DB_FOLDER, exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    """Create the finance_entries table if it doesn't already exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS finance_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            income REAL NOT NULL,
            expenses REAL NOT NULL,
            savings REAL NOT NULL,
            financial_goal TEXT,
            target_amount REAL,
            duration_months INTEGER,
            savings_rate REAL,
            expense_ratio REAL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def insert_entry(name, age, income, expenses, savings, financial_goal,
                  target_amount, duration_months, savings_rate, expense_ratio):
    """Insert one financial entry and return its new row id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO finance_entries (
            name, age, income, expenses, savings, financial_goal,
            target_amount, duration_months, savings_rate, expense_ratio, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name, age, income, expenses, savings, financial_goal,
        target_amount, duration_months, savings_rate, expense_ratio,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_all_entries():
    """Return all entries, most recent first, as a list of tuples."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM finance_entries ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_entries_by_name(name):
    """Return entries for one user, most recent first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM finance_entries WHERE name = ? ORDER BY id DESC", (name,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_all_names():
    """Return the distinct list of names that have entries."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM finance_entries ORDER BY name ASC")
    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return names


def get_latest_entry(name=None):
    """Return the most recent entry (optionally filtered by name), or None."""
    conn = get_connection()
    cursor = conn.cursor()
    if name:
        cursor.execute(
            "SELECT * FROM finance_entries WHERE name = ? ORDER BY id DESC LIMIT 1", (name,)
        )
    else:
        cursor.execute("SELECT * FROM finance_entries ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row


def delete_entry(entry_id):
    """Delete a single entry by its id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM finance_entries WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()


def get_column_names():
    """Column order for finance_entries — handy for building DataFrames."""
    return [
        "id", "name", "age", "income", "expenses", "savings", "financial_goal",
        "target_amount", "duration_months", "savings_rate", "expense_ratio", "created_at"
    ]
