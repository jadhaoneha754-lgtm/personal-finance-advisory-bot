"""
calculations.py
----------------
Pure financial calculation functions used across the app.
Keeping these separate from the UI (app.py) makes the logic easy
to test, reuse, and understand.
"""


def calculate_total_savings(income: float, expenses: float) -> float:
    """Monthly savings = income - expenses."""
    return round(income - expenses, 2)


def calculate_savings_rate(income: float, savings: float) -> float:
    """Savings rate (%) = (savings / income) * 100."""
    if income <= 0:
        return 0.0
    return round((savings / income) * 100, 2)


def calculate_expense_ratio(income: float, expenses: float) -> float:
    """Expense ratio (%) = (expenses / income) * 100."""
    if income <= 0:
        return 0.0
    return round((expenses / income) * 100, 2)


def calculate_yearly_savings(monthly_savings: float) -> float:
    """Simple projection: monthly savings * 12."""
    return round(monthly_savings * 12, 2)


def calculate_monthly_required_for_goal(target_amount: float, duration_months: int) -> float:
    """
    Amount that must be saved every month to hit `target_amount`
    within `duration_months`, assuming starting from zero.
    """
    if duration_months <= 0:
        return 0.0
    return round(target_amount / duration_months, 2)


def calculate_goal_progress(amount_saved_so_far: float, target_amount: float) -> float:
    """Progress (%) toward a goal, capped at 100%."""
    if target_amount <= 0:
        return 0.0
    progress = (amount_saved_so_far / target_amount) * 100
    return round(min(max(progress, 0), 100.0), 2)


def calculate_emergency_fund_target(expenses: float, months: int = 6) -> float:
    """Recommended emergency fund = `months` (default 6) of expenses."""
    return round(expenses * months, 2)
