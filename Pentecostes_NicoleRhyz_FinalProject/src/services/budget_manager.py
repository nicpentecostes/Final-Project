"""
budget_manager.py

Contains the BudgetManager class which handles all business logic for the
Budget Planner: setting budgets, logging transactions, generating summaries,
and providing spending alerts.
"""

from datetime import datetime
from models.budget import Budget
from models.transaction import Transaction
from services.file_handler import FileHandler


class BudgetManager:
    """Manages budgets and transactions for the CLI Budget Planner.

    Attributes:
        budgets (list[Budget]): List of monthly budget configurations.
        transactions (list[Transaction]): List of all recorded transactions.
    """

    VALID_TYPES = {"income", "expense"}

    def __init__(self):
        """Initializes BudgetManager and loads existing data from disk."""
        self.budgets: list[Budget] = []
        self.transactions: list[Transaction] = []
        self._load()

    # ------------------------------------------------------------------ #
    #  Private helpers                                                     #
    # ------------------------------------------------------------------ #

    def _load(self) -> None:
        """Loads budgets and transactions from the JSON file into memory."""
        data = FileHandler.load_data()

        self.budgets = [
            Budget(b["month"], b["income_goal"], b["spending_limit"])
            for b in data.get("budgets", [])
            if all(k in b for k in ("month", "income_goal", "spending_limit"))
        ]

        self.transactions = [
            Transaction(t["trans_type"], t["category"], t["amount"], t["date"], t.get("note", ""))
            for t in data.get("transactions", [])
            if all(k in t for k in ("trans_type", "category", "amount", "date"))
        ]

    def _save(self) -> None:
        """Persists current budgets and transactions to disk."""
        FileHandler.save_data({
            "budgets": [b.to_dict() for b in self.budgets],
            "transactions": [t.to_dict() for t in self.transactions],
        })

    @staticmethod
    def _validate_date(date_str: str) -> bool:
        """Validates a date string against YYYY-MM-DD format.

        Args:
            date_str (str): The date string to check.

        Returns:
            bool: True if valid, False otherwise.
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def _validate_month(month_str: str) -> bool:
        """Validates a month string against YYYY-MM format.

        Args:
            month_str (str): The month string to check.

        Returns:
            bool: True if valid, False otherwise.
        """
        try:
            datetime.strptime(month_str, "%Y-%m")
            return True
        except ValueError:
            return False

    def _get_budget(self, month: str) -> Budget | None:
        """Retrieves the budget for a given month.

        Args:
            month (str): Month in YYYY-MM format.

        Returns:
            Budget | None: Matching Budget or None if not set.
        """
        return next((b for b in self.budgets if b.month == month), None)

    def _month_totals(self, month: str) -> tuple[float, float]:
        """Calculates total income and total expenses for a given month.

        Uses a generator expression for memory-efficient summation.

        Args:
            month (str): Month in YYYY-MM format.

        Returns:
            tuple[float, float]: (total_income, total_expenses)
        """
        month_txns = [t for t in self.transactions if t.date.startswith(month)]

        total_income = sum(t.amount for t in month_txns if t.trans_type == "income")
        total_expenses = sum(t.amount for t in month_txns if t.trans_type == "expense")

        return total_income, total_expenses

    # ------------------------------------------------------------------ #
    #  Public interface                                                    #
    # ------------------------------------------------------------------ #

    def set_budget(self, month: str, income_goal: float, spending_limit: float) -> bool:
        """Creates or updates the budget for a given month.

        Args:
            month (str): Month in YYYY-MM format.
            income_goal (float): Target income for the month.
            spending_limit (float): Maximum spending allowed.

        Returns:
            bool: True if saved successfully, False on validation error.
        """
        if not self._validate_month(month):
            print("  [Error] Invalid month format. Use YYYY-MM.")
            return False

        if income_goal <= 0 or spending_limit <= 0:
            print("  [Error] Income goal and spending limit must be greater than zero.")
            return False

        existing = self._get_budget(month)
        if existing:
            existing.income_goal = round(income_goal, 2)
            existing.spending_limit = round(spending_limit, 2)
            print(f"  Budget for {month} updated.")
        else:
            self.budgets.append(Budget(month, income_goal, spending_limit))
            print(f"  Budget for {month} set.")

        self._save()
        return True

    def add_transaction(self, trans_type: str, category: str, amount: float,
                        date: str, note: str = "") -> bool:
        """Records a new income or expense transaction.

        Args:
            trans_type (str): 'income' or 'expense'.
            category (str): Transaction category.
            amount (float): Transaction amount (must be positive).
            date (str): Date in YYYY-MM-DD format.
            note (str): Optional note.

        Returns:
            bool: True if added successfully, False on validation error.
        """
        if trans_type.lower() not in self.VALID_TYPES:
            print("  [Error] Type must be 'income' or 'expense'.")
            return False

        if amount <= 0:
            print("  [Error] Amount must be greater than zero.")
            return False

        if not self._validate_date(date):
            print("  [Error] Invalid date format. Use YYYY-MM-DD.")
            return False

        txn = Transaction(trans_type, category, amount, date, note)
        self.transactions.append(txn)
        self._save()

        # Spending alert check
        if trans_type.lower() == "expense":
            month = date[:7]
            budget = self._get_budget(month)
            if budget:
                _, total_expenses = self._month_totals(month)
                if total_expenses > budget.spending_limit:
                    over = total_expenses - budget.spending_limit
                    print(f"  [!] WARNING: You have exceeded your spending limit by P{over:.2f}!")
                elif total_expenses >= budget.spending_limit * 0.9:
                    print(f"  [!] NOTICE: You are at 90%+ of your spending limit for {month}.")

        return True

    def view_transactions(self, month: str = "") -> None:
        """Displays all transactions, optionally filtered by month.

        Args:
            month (str): Optional YYYY-MM filter. Shows all if empty.
        """
        txns = (
            [t for t in self.transactions if t.date.startswith(month)]
            if month else self.transactions
        )

        if not txns:
            print("\n  No transactions found.\n")
            return

        label = f"TRANSACTIONS — {month}" if month else "ALL TRANSACTIONS"
        print(f"\n  {label}")
        print("  " + "-" * 58)
        print(f"  {'DATE':<12} {'T':<3} {'CATEGORY':<15} {'AMOUNT':>12}  NOTE")
        print("  " + "-" * 58)

        for txn in txns:
            print(f"  {txn}")

        print("  " + "-" * 58)
        total_in = sum(t.amount for t in txns if t.trans_type == "income")
        total_out = sum(t.amount for t in txns if t.trans_type == "expense")
        print(f"  {'Total Income':<28} P{total_in:>10.2f}")
        print(f"  {'Total Expenses':<28} P{total_out:>10.2f}")
        print(f"  {'Net':<28} P{total_in - total_out:>10.2f}\n")

    def view_budget_status(self, month: str) -> None:
        """Displays the budget status and remaining balance for a month.

        Args:
            month (str): Month in YYYY-MM format.
        """
        if not self._validate_month(month):
            print("  [Error] Invalid month format. Use YYYY-MM.")
            return

        budget = self._get_budget(month)
        total_income, total_expenses = self._month_totals(month)
        remaining = total_income - total_expenses

        print(f"\n  BUDGET STATUS — {month}")
        print("  " + "=" * 45)

        if budget:
            income_pct = (total_income / budget.income_goal * 100) if budget.income_goal else 0
            spend_pct = (total_expenses / budget.spending_limit * 100) if budget.spending_limit else 0
            print(f"  Income Goal    : P{budget.income_goal:>10.2f}")
            print(f"  Spending Limit : P{budget.spending_limit:>10.2f}")
            print("  " + "-" * 45)
            print(f"  Total Income   : P{total_income:>10.2f}  ({income_pct:.1f}% of goal)")
            print(f"  Total Expenses : P{total_expenses:>10.2f}  ({spend_pct:.1f}% of limit)")
        else:
            print("  No budget set for this month.")
            print("  " + "-" * 45)
            print(f"  Total Income   : P{total_income:>10.2f}")
            print(f"  Total Expenses : P{total_expenses:>10.2f}")

        print("  " + "-" * 45)
        status = "SURPLUS" if remaining >= 0 else "DEFICIT"
        print(f"  Net Balance    : P{remaining:>10.2f}  [{status}]")
        print("  " + "=" * 45 + "\n")

    def category_summary(self, month: str = "") -> None:
        """Displays a spending breakdown by category.

        Builds a category-total mapping using a dictionary and sorts
        by total amount descending.

        Args:
            month (str): Optional YYYY-MM filter. Uses all data if empty.
        """
        txns = (
            [t for t in self.transactions if t.date.startswith(month) and t.trans_type == "expense"]
            if month else [t for t in self.transactions if t.trans_type == "expense"]
        )

        if not txns:
            print("\n  No expense transactions found.\n")
            return

        # Build category totals using a dictionary
        totals: dict[str, float] = {}
        for t in txns:
            totals[t.category] = totals.get(t.category, 0.0) + t.amount

        grand_total = sum(totals.values())
        sorted_cats = sorted(totals.items(), key=lambda x: x[1], reverse=True)

        # Unique categories via a set
        unique_cats = {t.category for t in txns}

        label = f"CATEGORY BREAKDOWN — {month}" if month else "CATEGORY BREAKDOWN — ALL TIME"
        print(f"\n  {label}")
        print("  " + "=" * 48)
        print(f"  Categories: {len(unique_cats)}   Total Spent: P{grand_total:.2f}")
        print("  " + "-" * 48)
        print(f"  {'CATEGORY':<20} {'TOTAL':>10}   {'SHARE':>6}")
        print("  " + "-" * 48)

        for cat, total in sorted_cats:
            share = (total / grand_total) * 100
            print(f"  {cat:<20} P{total:>9.2f}   {share:>5.1f}%")

        print("  " + "=" * 48 + "\n")

    def delete_transaction(self, index: int) -> bool:
        """Removes a transaction by its 1-based display index.

        Args:
            index (int): 1-based position of the transaction to remove.

        Returns:
            bool: True if deleted, False if index is out of range.
        """
        if index < 1 or index > len(self.transactions):
            print(f"  [Error] Index {index} is out of range.")
            return False

        removed = self.transactions.pop(index - 1)
        self._save()
        print(f"  Deleted: {removed}\n")
        return True

    def sort_transactions(self, key: str = "date", descending: bool = False) -> None:
        """Displays transactions sorted by a chosen field.

        Args:
            key (str): Sort field — 'date', 'amount', or 'category'.
            descending (bool): True for descending order.
        """
        sort_keys = {
            "date": lambda t: t.date,
            "amount": lambda t: t.amount,
            "category": lambda t: t.category.lower(),
        }

        if key not in sort_keys:
            print(f"  [Error] Invalid sort key. Choose: date, amount, category.")
            return

        sorted_txns = sorted(self.transactions, key=sort_keys[key], reverse=descending)
        order = "Descending" if descending else "Ascending"

        print(f"\n  SORTED BY {key.upper()} ({order})")
        print("  " + "-" * 58)

        for txn in sorted_txns:
            print(f"  {txn}")

        print()
