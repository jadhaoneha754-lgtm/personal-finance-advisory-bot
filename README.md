# 💰 Personal Finance Advisory Bot

A beginner-friendly, rule-based web application that helps users understand
their monthly finances and gives simple, educational budgeting guidance —
built with **Python**, **Streamlit**, and **SQLite**.

---

## 📖 Description

Personal Finance Advisory Bot lets a user enter their monthly income,
expenses, savings, age, and a financial goal. The app then calculates key
financial ratios (savings rate, expense ratio, projected yearly savings,
goal-based monthly savings requirement) and generates plain-English
budgeting advice using a **rule-based engine** — no external AI API calls,
so it runs entirely offline once installed.

All monetary values are shown in **₹ (INR)**.

---

## ✨ Features

- **User Input Form** — name, age, income, expenses, savings, financial
  goal, target amount, and target duration.
- **Financial Calculations** — savings, savings rate, expense ratio,
  projected yearly savings, and required monthly savings for a goal.
- **Rule-Based Advisory System**
  - Classifies savings as Low / Moderate / Healthy
  - Classifies expense load as Comfortable / Moderate / High / Critical
  - Gives budgeting suggestions (e.g. the 50/30/20 rule)
  - Suggests an emergency-fund target (6 months of expenses)
  - Gives goal-based savings guidance
  - **Does NOT** give personalized investment, stock, or crypto advice
- **Interactive Dashboard** — income/expense/savings metrics, pie and bar
  charts, and goal progress bar.
- **Goal Planner** — stand-alone calculator for "how much do I need to save
  per month to hit X by Y months?"
- **History Page** — view and delete past entries stored in SQLite.
- **Input Validation** — no negative numbers, required fields enforced, and
  a warning (not a hard block) when expenses exceed income.

---

## 🛠 Technologies

| Tool | Purpose |
|---|---|
| Python 3.9+ | Core language |
| Streamlit | Web UI / frontend |
| SQLite | Local database (auto-created) |
| Pandas | Tabular data handling |
| Plotly | Interactive charts |

---

## 📁 Project Structure

```
personal-finance-advisory-bot/
│
├── app.py              # Streamlit UI, page navigation, forms, charts
├── database.py          # SQLite connection, table creation, CRUD helpers
├── advisor.py            # Rule-based advisory / suggestion logic
├── calculations.py        # Pure financial math functions
├── sample_data.py          # Optional: preload a few sample entries
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── .gitignore                # Files/folders excluded from git
└── data/
    └── .gitkeep                # Keeps the empty folder in git;
                                  finance.db is created here at runtime
```

**Why split into files like this?**
- `calculations.py` holds only math — easy to unit test.
- `advisor.py` turns numbers into human-readable advice — easy to extend
  with new rules later (or eventually swap in a real ML model).
- `database.py` isolates all SQL — the rest of the app never writes raw SQL.
- `app.py` is only responsible for the UI and wiring the pieces together.

---

## ⚙️ Installation

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/<your-username>/personal-finance-advisory-bot.git
   cd personal-finance-advisory-bot
   ```

2. **(Recommended) Create a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ How to Run

```bash
streamlit run app.py
```

Streamlit will print a local URL (usually `http://localhost:8501`) —
open it in your browser. The SQLite database (`data/finance.db`) and its
table are created automatically the first time the app starts, so there
is no manual database setup.

### Optional: load sample data first

To immediately see the Dashboard and History pages populated with example
users:

```bash
python sample_data.py
streamlit run app.py
```

---

## 🧪 Example Usage

1. Open the app and go to **🧭 Finance Advisor** in the sidebar.
2. Fill in the form, e.g.:
   - Name: `Aarav Sharma`
   - Age: `21`
   - Monthly Income: `₹25,000`
   - Monthly Expenses: `₹18,000`
   - Monthly Savings: `₹7,000`
   - Financial Goal: `Build an emergency fund`
   - Target Amount: `₹60,000`
   - Target Duration: `8` months
3. Click **Analyze My Finances** to see your savings rate, expense ratio,
   charts, and a full advisory report.
4. Visit **🏠 Dashboard** to see a visual summary, **🎯 Goal Planner** to
   experiment with different targets/timelines, and **📜 History** to
   review or delete past entries.

---

## 🚀 Future Improvements

- Replace the rule-based advisor with a trained ML model (e.g. a
  classifier for spending patterns) as a v2.
- Add user authentication so multiple people can keep private histories.
- Add expense-category breakdown (rent, food, transport, etc.) instead of
  a single "expenses" number.
- Add monthly trend charts once a user has multiple entries over time.
- Export reports as PDF.
- Add multi-currency support beyond ₹ (INR).

---

## ⚠️ Disclaimer

This project is built for **educational purposes only**, as part of an
AI/ML engineering student's portfolio. It uses simple rule-based logic and
does **not** provide personalized financial, investment, tax, or legal
advice. Always consult a qualified, licensed financial advisor before
making real financial decisions.
