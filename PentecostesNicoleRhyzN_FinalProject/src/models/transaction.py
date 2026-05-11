"""
transaction.py

Defines the Transaction model representing a single income or expense entry.
"""


class Transaction:
    """Represents a single financial transaction.

    Attributes:
        trans_type (str): Either 'income' or 'expense'.
        category (str): Category label (e.g., Food, Salary, Rent).
        amount (float): Monetary value of the transaction.
        date (str): Date in YYYY-MM-DD format.
        note (str): Optional short description.
    """

    def __init__(self, trans_type: str, category: str, amount: float, date: str, note: str = ""):
        """Initializes a Transaction instance.

        Args:
            trans_type (str): 'income' or 'expense'.
            category (str): The transaction category.
            amount (float): The transaction amount.
            date (str): Date in YYYY-MM-DD format.
            note (str): Optional note. Defaults to empty string.
        """
        self.trans_type = trans_type.lower()
        self.category = category.strip().title()
        self.amount = round(amount, 2)
        self.date = date
        self.note = note.strip()

    def to_dict(self) -> dict:
        """Serializes the transaction to a dictionary.

        Returns:
            dict: Dictionary representation of the transaction.
        """
        return {
            "trans_type": self.trans_type,
            "category": self.category,
            "amount": self.amount,
            "date": self.date,
            "note": self.note,
        }

    def __str__(self) -> str:
        """Returns a formatted string representation of the transaction.

        Returns:
            str: Human-readable transaction line.
        """
        tag = "+" if self.trans_type == "income" else "-"
        note_str = f"  ({self.note})" if self.note else ""
        return f"{self.date} | {tag} | {self.category:<15} | P{self.amount:>10.2f}{note_str}"
