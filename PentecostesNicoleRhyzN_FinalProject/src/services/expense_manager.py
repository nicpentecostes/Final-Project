"""
expense_manager.py

Contains the ExpenseManager class which handles all business logic
for managing expenses: adding, viewing, searching, sorting, filtering,
deleting, and generating summary reports.
"""

from datetime import datetime
from models.expense import Expense
from services.file_handler import FileHandler


class ExpenseManager:
    """Manages a collection of Expense objects and coordinates persistence.

    Attributes:
        expenses (list[Expense]): In-memory list of all loaded expenses.
        _category_totals (dict[str, float]): Cached totals per category,
            rebuilt on each report generation.
    """

    def __init__(self):
        """Initializes ExpenseManager and loads existing data from disk."""
        self.expenses: list[Expense] = []
        self._category_totals: dict[str, float] = {}
        self._load_from_file()

    # ------------------------------------------------------------------ #
    #  Private helpers                                                     #
    # ------------------------------------------------------------------ #

    def _load_from_file(self) -> None:
        """Loads expense records from the JSON file into memory."""
        data = FileHandler.load_data()
        self.expenses = [
            Expense(item["category"], item["amount"], item["date"])
            for item in data
            if all(k in item for k in ("category", "amount", "date"))
        ]

    def _save(self) -> None:
        """Persists the current in-memory expenses list to disk."""
        FileHandler.save_data([e.to_dict() for e in self.expenses])

    def _build_category_totals(self) -> dict[str, float]:
        """Aggregates total spending per category using a dictionary.

        Returns:
            dict[str, float]: Mapping of category name to total amount.
        """
        totals: dict[str, float] = {}
        for expense in self.expenses:
            key = expense.category.title()
            totals[key] = totals.get(key, 0.0) + expense.amount
        return totals

    @staticmethod
    def _validate_date(date_str: str) -> bool:
        """Validates that a date string matches the YYYY-MM-DD format.

        Args:
            date_str (str): The date string to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    # ------------------------------------------------------------------ #
    #  Public interface                                                    #
    # ------------------------------------------------------------------ #

    def add_expense(self, category: str, amount: float, date: str) -> bool:
        """Creates and stores a new expense entry.

        Args:
            category (str): The expense category.
            amount (float): The expense amount (must be positive).
            date (str): The expense date in YYYY-MM-DD format.

        Returns:
            bool: True if added successfully, False if validation fails.
        """
        if amount <= 0:
            print("  [Error] Amount must be greater than zero.")
            return False

        if not self._validate_date(date):
            print("  [Error] Invalid date format. Use YYYY-MM-DD.")
            return False

        expense = Expense(category.strip().title(), round(amount, 2), date)
        self.expenses.append(expense)
        self._save()
        return True

    def view_expenses(self) -> None:
        """Displays all stored expenses in a formatted table."""
        if not self.expenses:
            print("\n  No expenses recorded yet.\n")
            return

        print("\n  EXPENSE LIST")
        print("  " + "-" * 50)
        print(f"  {'DATE':<12} {'CATEGORY':<15} {'AMOUNT':>12}")
        print("  " + "-" * 50)

        for expense in self.expenses:
            print(f"  {expense}")

        print("  " + "-" * 50)
        total = sum(e.amount for e in self.expenses)
        print(f"  {'TOTAL':<28} P{total:>10.2f}\n")

    def search_by_category(self, category: str) -> None:
        """Searches and displays expenses matching a given category.

        Uses a list comprehension to filter results case-insensitively.

        Args:
            category (str): The category name to search for.
        """
        results = [
            e for e in self.expenses
            if e.category.lower() == category.strip().lower()
        ]

        if not results:
            print(f"\n  No expenses found under '{category}'.\n")
            return

        print(f"\n  RESULTS FOR: {category.title()}")
        print("  " + "-" * 50)

        for expense in results:
            print(f"  {expense}")

        subtotal = sum(e.amount for e in results)
        print("  " + "-" * 50)
        print(f"  Subtotal: P{subtotal:.2f}\n")

    def search_by_date_range(self, start: str, end: str) -> None:
        """Filters and displays expenses within a date range (inclusive).

        Args:
            start (str): Start date in YYYY-MM-DD format.
            end (str): End date in YYYY-MM-DD format.
        """
        if not self._validate_date(start) or not self._validate_date(end):
            print("  [Error] Invalid date format. Use YYYY-MM-DD.")
            return

        start_dt = datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.strptime(end, "%Y-%m-%d")

        if start_dt > end_dt:
            print("  [Error] Start date must be before or equal to end date.")
            return

        results = [
            e for e in self.expenses
            if start_dt <= datetime.strptime(e.date, "%Y-%m-%d") <= end_dt
        ]

        if not results:
            print(f"\n  No expenses found between {start} and {end}.\n")
            return

        print(f"\n  EXPENSES FROM {start} TO {end}")
        print("  " + "-" * 50)

        for expense in results:
            print(f"  {expense}")

        subtotal = sum(e.amount for e in results)
        print("  " + "-" * 50)
        print(f"  Subtotal: P{subtotal:.2f}\n")

    def sort_expenses(self, key: str = "amount", descending: bool = True) -> None:
        """Displays expenses sorted by a given field.

        Supports sorting by 'amount', 'date', or 'category'.

        Args:
            key (str): The field to sort by. Defaults to 'amount'.
            descending (bool): Sort order. Defaults to True (highest first).
        """
        sort_keys = {
            "amount": lambda e: e.amount,
            "date": lambda e: e.date,
            "category": lambda e: e.category.lower(),
        }

        if key not in sort_keys:
            print(f"  [Error] Invalid sort key '{key}'. Choose: amount, date, category.")
            return

        sorted_expenses = sorted(self.expenses, key=sort_keys[key], reverse=descending)
        order_label = "Descending" if descending else "Ascending"

        print(f"\n  SORTED BY {key.upper()} ({order_label})")
        print("  " + "-" * 50)

        for expense in sorted_expenses:
            print(f"  {expense}")

        print()

    def delete_expense(self, index: int) -> bool:
        """Removes an expense by its 1-based display index.

        Args:
            index (int): The 1-based position of the expense to delete.

        Returns:
            bool: True if deleted, False if index is out of range.
        """
        if index < 1 or index > len(self.expenses):
            print(f"  [Error] Index {index} is out of range.")
            return False

        removed = self.expenses.pop(index - 1)
        self._save()
        print(f"  Deleted: {removed}\n")
        return True

    def generate_report(self) -> None:
        """Generates a summary report grouped by category.

        Builds a category-total mapping and displays spending breakdown
        with percentage share per category, sorted by total descending.
        """
        if not self.expenses:
            print("\n  No expenses to report.\n")
            return

        self._category_totals = self._build_category_totals()
        grand_total = sum(self._category_totals.values())

        # Sort categories by total amount descending
        sorted_categories = sorted(
            self._category_totals.items(),
            key=lambda item: item[1],
            reverse=True
        )

        # Unique categories using a set
        unique_categories = {e.category for e in self.expenses}

        print("\n  EXPENSE REPORT")
        print("  " + "=" * 50)
        print(f"  Total Entries   : {len(self.expenses)}")
        print(f"  Categories Used : {len(unique_categories)}")
        print(f"  Grand Total     : P{grand_total:.2f}")
        print("  " + "-" * 50)
        print(f"  {'CATEGORY':<20} {'TOTAL':>10}   {'SHARE':>6}")
        print("  " + "-" * 50)

        for cat, total in sorted_categories:
            share = (total / grand_total) * 100
            print(f"  {cat:<20} P{total:>9.2f}   {share:>5.1f}%")

        print("  " + "=" * 50 + "\n")
