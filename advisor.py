"""
advisor.py
----------
A simple RULE-BASED advisory engine (no ML, no AI API calls).
It turns numbers from calculations.py into plain-English,
educational budgeting suggestions.

IMPORTANT: This module intentionally does NOT give investment,
stock, or crypto recommendations. It only offers general
budgeting education, as required by the project scope.
"""

from calculations import (
    calculate_emergency_fund_target,
    calculate_monthly_required_for_goal,
)


def get_savings_health(savings_rate: float) -> str:
    """Classify savings rate into Low / Moderate / Healthy."""
    if savings_rate < 10:
        return "Low"
    elif savings_rate < 25:
        return "Moderate"
    else:
        return "Healthy"


def get_expense_health(expense_ratio: float) -> str:
    """Classify how much of income is consumed by expenses."""
    if expense_ratio > 90:
        return "Critical"
    elif expense_ratio > 70:
        return "High"
    elif expense_ratio > 50:
        return "Moderate"
    else:
        return "Comfortable"


def generate_budget_suggestions(income, expenses, savings, savings_rate, expense_ratio):
    """Return a list of plain-English budgeting suggestions."""
    suggestions = []

    if expenses > income:
        suggestions.append(
            "⚠️ Your expenses exceed your income. This is not sustainable long-term — "
            "review your spending categories and identify non-essential costs to trim first."
        )

    if savings_rate < 10:
        suggestions.append(
            "Your savings rate is on the lower side. A common beginner target is to save "
            "at least 10–20% of your income. Tracking where your money goes for a month "
            "usually reveals quick wins."
        )
    elif savings_rate < 25:
        suggestions.append(
            "You're saving a moderate share of your income. Consider gradually working "
            "toward 20–30% as your income grows or expenses reduce."
        )
    else:
        suggestions.append(
            "You're saving a healthy portion of your income — nice work! Keep this "
            "consistency and consider directing any surplus toward your goals."
        )

    if expense_ratio > 70:
        suggestions.append(
            "A large share of your income goes to expenses. The 50/30/20 rule "
            "(50% needs, 30% wants, 20% savings) is a simple guideline to reorganize a budget."
        )

    if savings <= 0:
        suggestions.append(
            "You currently have no monthly surplus. Focus on balancing income and expenses "
            "before setting aggressive savings goals."
        )

    return suggestions


def generate_emergency_fund_advice(expenses: float) -> str:
    target = calculate_emergency_fund_target(expenses)
    return (
        f"An emergency fund of about ₹{target:,.2f} (6 months of expenses) is generally "
        "recommended to cover unexpected situations like medical emergencies or job loss."
    )


def generate_goal_advice(target_amount: float, duration_months: int, current_monthly_savings: float) -> str:
    """Goal-based savings guidance — purely arithmetic, no market advice."""
    if target_amount <= 0 or duration_months <= 0:
        return "Enter a valid target amount and duration to get goal-based guidance."

    required_monthly = calculate_monthly_required_for_goal(target_amount, duration_months)

    if current_monthly_savings <= 0:
        return (
            f"To reach ₹{target_amount:,.2f} in {duration_months} month(s), you'd need to save "
            f"about ₹{required_monthly:,.2f}/month. You currently have no monthly surplus, so "
            "revisiting your budget first is a good starting point."
        )

    if current_monthly_savings >= required_monthly:
        return (
            f"You're on track! Reaching ₹{target_amount:,.2f} in {duration_months} month(s) "
            f"needs about ₹{required_monthly:,.2f}/month, and your current savings of "
            f"₹{current_monthly_savings:,.2f}/month already covers that."
        )

    gap = round(required_monthly - current_monthly_savings, 2)
    return (
        f"Reaching ₹{target_amount:,.2f} in {duration_months} month(s) needs about "
        f"₹{required_monthly:,.2f}/month. You're currently saving ₹{current_monthly_savings:,.2f}/month "
        f"— a gap of ₹{gap:,.2f}/month. Consider extending the timeline or trimming expenses."
    )


def generate_full_report(income, expenses, savings, savings_rate, expense_ratio,
                          target_amount, duration_months):
    """Bundle every piece of advice into one dictionary for the UI to render."""
    return {
        "savings_health": get_savings_health(savings_rate),
        "expense_health": get_expense_health(expense_ratio),
        "budget_suggestions": generate_budget_suggestions(
            income, expenses, savings, savings_rate, expense_ratio
        ),
        "emergency_fund_advice": generate_emergency_fund_advice(expenses),
        "goal_advice": generate_goal_advice(target_amount, duration_months, savings),
    }
