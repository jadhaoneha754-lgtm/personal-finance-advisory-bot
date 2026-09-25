"""
sample_data.py
--------------
Optional helper script that inserts a few sample entries into the
database so you can immediately explore the Dashboard and History
pages without filling the form by hand.

Run with:
    python sample_data.py
"""

import database as db
import calculations as calc

SAMPLE_USERS = [
    {
        "name": "Aarav Sharma",
        "age": 21,
        "income": 25000,
        "expenses": 18000,
        "savings": 7000,
        "financial_goal": "Build an emergency fund",
        "target_amount": 60000,
        "duration_months": 8,
    },
    {
        "name": "Priya Nair",
        "age": 22,
        "income": 40000,
        "expenses": 22000,
        "savings": 18000,
        "financial_goal": "Save for a trip",
        "target_amount": 50000,
        "duration_months": 4,
    },
    {
        "name": "Rohan Mehta",
        "age": 20,
        "income": 15000,
        "expenses": 16000,
        "savings": 0,
        "financial_goal": "General savings",
        "target_amount": 20000,
        "duration_months": 12,
    },
]


def load_sample_data():
    db.init_db()
    for user in SAMPLE_USERS:
        savings_rate = calc.calculate_savings_rate(user["income"], user["savings"])
        expense_ratio = calc.calculate_expense_ratio(user["income"], user["expenses"])
        db.insert_entry(
            user["name"], user["age"], user["income"], user["expenses"],
            user["savings"], user["financial_goal"], user["target_amount"],
            user["duration_months"], savings_rate, expense_ratio,
        )
    print(f"Inserted {len(SAMPLE_USERS)} sample entries into the database.")


if __name__ == "__main__":
    load_sample_data()
