# CLI Budget Planner

A command-line application for managing personal monthly budgets. Set income goals and spending limits, log transactions, and track your financial health — all from the terminal.

---

## Features

- Set a monthly budget with an income goal and spending limit
- Log income and expense transactions with category, date, and optional note
- View all transactions (filterable by month)
- View budget status with income vs. spending progress and net balance
- Category breakdown with percentage share of total spending
- Sort transactions by date, amount, or category
- Delete a transaction by index
- Spending alerts when you hit 90% or exceed your monthly limit
- Persistent storage via JSON file
- Full input validation and error handling

---

## Project Structure

```
<LastName_FirstName>_FinalProject/
├── README.md
├── src/
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── budget.py
│   │   └── transaction.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── budget_manager.py
│   │   └── file_handler.py
│   └── data/
│       └── budget_data.json
```

---

## Setup & Installation

No external dependencies required. Uses only Python standard library (`json`, `os`, `datetime`).

**Requirements:** Python 3.10 or higher

```bash
# Clone the repository
git clone https://github.com/<your-username>/<LastName_FirstName>_FinalProject.git
cd <LastName_FirstName>_FinalProject

# Run the application
py src/main.py
```

---

## Sample CLI Usage

```
  Welcome to CLI Budget Planner!

==========================================
        CLI BUDGET PLANNER
==========================================
  1. Set Monthly Budget
  2. Add Transaction (Income/Expense)
  3. View Transactions
  4. View Budget Status
  5. Category Breakdown
  6. Sort Transactions
  7. Delete a Transaction
  8. Exit
==========================================
  Enter choice: 1

  -- Set Monthly Budget --
  Month (YYYY-MM): 2026-05
  Income goal: 30000
  Spending limit: 20000
  Budget for 2026-05 set.
```

```
  BUDGET STATUS — 2026-05
  =============================================
  Income Goal    :  P30000.00
  Spending Limit :  P20000.00
  ---------------------------------------------
  Total Income   :  P30000.00  (100.0% of goal)
  Total Expenses :  P12500.00  (62.5% of limit)
  ---------------------------------------------
  Net Balance    :  P17500.00  [SURPLUS]
  =============================================
```

---

## Video Demonstration

> YouTube URL: *(to be added after recording)*

---

## Author

*(Your Name)*
*(Course & Section)*
*(Date)*
