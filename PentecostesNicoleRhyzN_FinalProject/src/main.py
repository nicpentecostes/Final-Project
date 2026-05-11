"""
main.py

Entry point for the CLI Budget Planner application.
Provides an interactive menu-driven interface for managing budgets
and tracking income and expense transactions.

Run with:
    py src/main.py
"""

from services.budget_manager import BudgetManager


def display_menu() -> None:
    """Prints the main navigation menu to the console."""
    print("\n" + "=" * 42)
    print("        CLI BUDGET PLANNER")
    print("=" * 42)
    print("  1. Set Monthly Budget")
    print("  2. Add Transaction (Income/Expense)")
    print("  3. View Transactions")
    print("  4. View Budget Status")
    print("  5. Category Breakdown")
    print("  6. Sort Transactions")
    print("  7. Delete a Transaction")
    print("  8. Exit")
    print("=" * 42)


def get_month_input(prompt: str = "  Month (YYYY-MM, or Enter to skip): ") -> str:
    """Prompts the user for an optional month filter.

    Args:
        prompt (str): The input prompt to display.

    Returns:
        str: The entered month string, or empty string if skipped.
    """
    return input(prompt).strip()


def main() -> None:
    """Main loop that drives the CLI Budget Planner application.

    Instantiates BudgetManager and continuously presents the menu
    until the user chooses to exit.
    """
    manager = BudgetManager()
    print("\n  Welcome to CLI Budget Planner!")

    while True:
        display_menu()
        choice = input("  Enter choice: ").strip()

        # ── 1. Set Monthly Budget ──────────────────────────────────────
        if choice == "1":
            print("\n  -- Set Monthly Budget --")
            month = input("  Month (YYYY-MM): ").strip()

            try:
                income_goal = float(input("  Income goal: ").strip())
                spending_limit = float(input("  Spending limit: ").strip())
            except ValueError:
                print("  [Error] Amounts must be numbers.")
                continue

            manager.set_budget(month, income_goal, spending_limit)

        # ── 2. Add Transaction ─────────────────────────────────────────
        elif choice == "2":
            print("\n  -- Add Transaction --")
            print("  Type: (I)ncome or (E)xpense")
            raw_type = input("  Enter I or E: ").strip().upper()

            if raw_type == "I":
                trans_type = "income"
            elif raw_type == "E":
                trans_type = "expense"
            else:
                print("  [Error] Enter I for income or E for expense.")
                continue

            category = input("  Category: ").strip()
            if not category:
                print("  [Error] Category cannot be empty.")
                continue

            try:
                amount = float(input("  Amount: ").strip())
            except ValueError:
                print("  [Error] Amount must be a number.")
                continue

            date = input("  Date (YYYY-MM-DD): ").strip()
            note = input("  Note (optional, press Enter to skip): ").strip()

            if manager.add_transaction(trans_type, category, amount, date, note):
                print("  Transaction recorded successfully.")

        # ── 3. View Transactions ───────────────────────────────────────
        elif choice == "3":
            month = get_month_input("  Filter by month (YYYY-MM, or Enter for all): ")
            manager.view_transactions(month)

        # ── 4. Budget Status ───────────────────────────────────────────
        elif choice == "4":
            month = input("  Month (YYYY-MM): ").strip()
            manager.view_budget_status(month)

        # ── 5. Category Breakdown ──────────────────────────────────────
        elif choice == "5":
            month = get_month_input("  Filter by month (YYYY-MM, or Enter for all): ")
            manager.category_summary(month)

        # ── 6. Sort Transactions ───────────────────────────────────────
        elif choice == "6":
            print("\n  Sort by:")
            print("    1. Date")
            print("    2. Amount")
            print("    3. Category")
            key_map = {"1": "date", "2": "amount", "3": "category"}
            key_choice = input("  Choose (1-3): ").strip()
            key = key_map.get(key_choice, "date")

            order = input("  Order — (A)scending or (D)escending [A]: ").strip().upper()
            descending = order == "D"

            manager.sort_transactions(key=key, descending=descending)

        # ── 7. Delete Transaction ──────────────────────────────────────
        elif choice == "7":
            manager.view_transactions()
            if manager.transactions:
                try:
                    index = int(input("  Enter number of transaction to delete: ").strip())
                    manager.delete_transaction(index)
                except ValueError:
                    print("  [Error] Please enter a valid number.")

        # ── 8. Exit ────────────────────────────────────────────────────
        elif choice == "8":
            print("\n  Goodbye!\n")
            break

        else:
            print("  [Error] Invalid choice. Enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
