"""
expense.py

Defines the Expense model representing a single expense entry.
"""


class Expense:
    """Represents a single expense entry with a category, amount, and date.

    Attributes:
        category (str): The category of the expense (e.g., Food, Transport).
        amount (float): The monetary amount of the expense.
        date (str): The date of the expense in YYYY-MM-DD format.
    """

    def __init__(self, category: str, amount: float, date: str):
        """Initializes an Expense instance.

        Args:
            category (str): The expense category.
            amount (float): The expense amount.
            date (str): The expense date in YYYY-MM-DD format.
        """
        self.category = category
        self.amount = amount
        self.date = date

    def to_dict(self) -> dict:
        """Serializes the expense to a dictionary.

        Returns:
            dict: A dictionary representation of the expense.
        """
        return {
            "category": self.category,
            "amount": self.amount,
            "date": self.date,
        }

    def __str__(self) -> str:
        """Returns a human-readable string representation of the expense.

        Returns:
            str: Formatted expense string.
        """
        return f"{self.date} | {self.category:<15} | P{self.amount:>10.2f}"
