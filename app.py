"""
app.py
------
Main Streamlit entry point for the Personal Finance Advisory Bot.

Run with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px

import database as db
import calculations as calc
import advisor

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Personal Finance Advisory Bot",
    page_icon="💰",
    layout="wide",
)

db.init_db()  # creates data/finance.db and the table if they don't exist yet

GOAL_OPTIONS = [
    "Build an emergency fund",
    "Save for education",
    "Save for a gadget/vehicle",
    "Save for a trip",
    "Save for a house down payment",
    "General savings",
    "Other",
]

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
st.sidebar.title("💰 Finance Advisory Bot")
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Dashboard", "🧭 Finance Advisor", "🎯 Goal Planner", "📜 History"],
)
st.sidebar.markdown("---")
st.sidebar.caption(
    "Educational budgeting tool. Not a substitute for professional "
    "financial advice. All amounts are in ₹ (INR)."
)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------
def entry_to_dict(row):
    """Turn a raw DB tuple into a dict using the known column order."""
    cols = db.get_column_names()
    return dict(zip(cols, row))


def validate_inputs(name, age, income, expenses, savings, target_amount, duration_months):
    """Return a list of error messages; empty list means input is valid."""
    errors = []
    if not name or not name.strip():
        errors.append("Name is required.")
    if age is None or age <= 0:
        errors.append("Age must be a positive number.")
    if income is None or income < 0:
        errors.append("Income cannot be negative.")
    if expenses is None or expenses < 0:
        errors.append("Expenses cannot be negative.")
    if savings is None or savings < 0:
        errors.append("Savings cannot be negative.")
    if target_amount is not None and target_amount < 0:
        errors.append("Target amount cannot be negative.")
    if duration_months is not None and duration_months < 0:
        errors.append("Target duration cannot be negative.")
    return errors


def render_summary_charts(income, expenses, savings):
    """Render a pie chart (expense split) and a bar chart (income vs expenses vs savings)."""
    col1, col2 = st.columns(2)

    with col1:
        pie_df = pd.DataFrame({
            "Category": ["Expenses", "Savings"],
            "Amount": [max(expenses, 0), max(savings, 0)],
        })
        fig_pie = px.pie(
            pie_df, names="Category", values="Amount",
            title="Expenses vs Savings", hole=0.4,
            color="Category",
            color_discrete_map={"Expenses": "#EF553B", "Savings": "#00CC96"},
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        bar_df = pd.DataFrame({
            "Category": ["Income", "Expenses", "Savings"],
            "Amount": [income, expenses, savings],
        })
        fig_bar = px.bar(
            bar_df, x="Category", y="Amount", title="Monthly Overview (₹)",
            color="Category", text_auto=".2s",
            color_discrete_map={"Income": "#636EFA", "Expenses": "#EF553B", "Savings": "#00CC96"},
        )
        st.plotly_chart(fig_bar, use_container_width=True)


# ---------------------------------------------------------------------------
# Page: Dashboard
# ---------------------------------------------------------------------------
if page == "🏠 Dashboard":
    st.title("🏠 Dashboard")

    names = db.get_all_names()
    if not names:
        st.info("No data yet. Go to **Finance Advisor** to add your first entry.")
    else:
        selected_name = st.selectbox("Select user", names)
        latest = db.get_latest_entry(selected_name)
        entry = entry_to_dict(latest)

        st.subheader(f"Latest snapshot for {entry['name']}")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Income", f"₹{entry['income']:,.2f}")
        m2.metric("Expenses", f"₹{entry['expenses']:,.2f}")
        m3.metric("Savings", f"₹{entry['savings']:,.2f}")
        m4.metric("Savings Rate", f"{entry['savings_rate']:.2f}%")

        render_summary_charts(entry["income"], entry["expenses"], entry["savings"])

        if entry["target_amount"] and entry["duration_months"]:
            progress = calc.calculate_goal_progress(
                entry["savings"] * entry["duration_months"], entry["target_amount"]
            )
            st.subheader(f"Goal: {entry['financial_goal']}")
            st.progress(int(progress))
            st.caption(
                f"Estimated progress toward ₹{entry['target_amount']:,.2f} "
                f"over {entry['duration_months']} months: {progress:.2f}%"
            )


# ---------------------------------------------------------------------------
# Page: Finance Advisor (input form + rule-based report)
# ---------------------------------------------------------------------------
elif page == "🧭 Finance Advisor":
    st.title("🧭 Finance Advisor")
    st.write("Enter your monthly finances below to get instant, educational budgeting advice.")

    with st.form("finance_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name *")
            age = st.number_input("Age *", min_value=0, max_value=120, step=1)
            income = st.number_input("Monthly Income (₹) *", min_value=0.0, step=500.0, format="%.2f")
            expenses = st.number_input("Monthly Expenses (₹) *", min_value=0.0, step=500.0, format="%.2f")
        with col2:
            savings = st.number_input("Monthly Savings (₹) *", min_value=0.0, step=500.0, format="%.2f")
            financial_goal = st.selectbox("Financial Goal", GOAL_OPTIONS)
            target_amount = st.number_input("Target Amount (₹)", min_value=0.0, step=1000.0, format="%.2f")
            duration_months = st.number_input("Target Duration (months)", min_value=0, step=1)

        submitted = st.form_submit_button("Analyze My Finances")

    if submitted:
        errors = validate_inputs(name, age, income, expenses, savings, target_amount, duration_months)

        if expenses > income:
            st.warning("⚠️ Your expenses are greater than your income.")

        if errors:
            for err in errors:
                st.error(err)
        else:
            savings_rate = calc.calculate_savings_rate(income, savings)
            expense_ratio = calc.calculate_expense_ratio(income, expenses)
            yearly_savings = calc.calculate_yearly_savings(savings)

            db.insert_entry(
                name, int(age), income, expenses, savings, financial_goal,
                target_amount, int(duration_months), savings_rate, expense_ratio
            )

            st.success("Entry saved! Here is your report:")

            m1, m2, m3 = st.columns(3)
            m1.metric("Savings Rate", f"{savings_rate:.2f}%")
            m2.metric("Expense Ratio", f"{expense_ratio:.2f}%")
            m3.metric("Est. Yearly Savings", f"₹{yearly_savings:,.2f}")

            render_summary_charts(income, expenses, savings)

            report = advisor.generate_full_report(
                income, expenses, savings, savings_rate, expense_ratio,
                target_amount, int(duration_months)
            )

            st.subheader("📋 Advisory Report")
            st.write(f"**Savings Health:** {report['savings_health']}")
            st.write(f"**Expense Health:** {report['expense_health']}")

            st.markdown("**Budgeting Suggestions:**")
            for s in report["budget_suggestions"]:
                st.write(f"- {s}")

            st.markdown("**Emergency Fund:**")
            st.write(report["emergency_fund_advice"])

            st.markdown("**Goal Guidance:**")
            st.write(report["goal_advice"])

            st.caption(
                "This is general educational guidance based on simple rules, "
                "not personalized financial or investment advice."
            )


# ---------------------------------------------------------------------------
# Page: Goal Planner
# ---------------------------------------------------------------------------
elif page == "🎯 Goal Planner":
    st.title("🎯 Goal Planner")
    st.write("Plan how much you need to save each month to hit a specific target.")

    col1, col2 = st.columns(2)
    with col1:
        target_amount = st.number_input("Target Amount (₹)", min_value=0.0, step=1000.0, format="%.2f")
        duration_months = st.number_input("Duration (months)", min_value=0, step=1)
    with col2:
        current_monthly_savings = st.number_input(
            "Your current monthly savings (₹)", min_value=0.0, step=500.0, format="%.2f"
        )
        amount_saved_so_far = st.number_input(
            "Amount already saved toward this goal (₹)", min_value=0.0, step=500.0, format="%.2f"
        )

    if st.button("Calculate Plan"):
        if target_amount <= 0 or duration_months <= 0:
            st.error("Please enter a valid target amount and duration.")
        else:
            required_monthly = calc.calculate_monthly_required_for_goal(target_amount, int(duration_months))
            progress = calc.calculate_goal_progress(amount_saved_so_far, target_amount)

            m1, m2 = st.columns(2)
            m1.metric("Required Monthly Savings", f"₹{required_monthly:,.2f}")
            m2.metric("Current Progress", f"{progress:.2f}%")

            st.progress(int(progress))

            st.markdown("**Guidance:**")
            st.write(
                advisor.generate_goal_advice(target_amount, int(duration_months), current_monthly_savings)
            )


# ---------------------------------------------------------------------------
# Page: History
# ---------------------------------------------------------------------------
elif page == "📜 History":
    st.title("📜 History")

    rows = db.get_all_entries()
    if not rows:
        st.info("No entries yet. Add one from the Finance Advisor page.")
    else:
        df = pd.DataFrame(rows, columns=db.get_column_names())
        st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.subheader("Delete an entry")
        entry_id_to_delete = st.number_input("Entry ID to delete", min_value=0, step=1)
        if st.button("Delete Entry"):
            if entry_id_to_delete in df["id"].values:
                db.delete_entry(int(entry_id_to_delete))
                st.success(f"Entry {int(entry_id_to_delete)} deleted. Refresh the page to see the update.")
            else:
                st.error("No entry found with that ID.")
