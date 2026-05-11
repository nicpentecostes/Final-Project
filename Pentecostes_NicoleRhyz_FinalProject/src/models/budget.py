"""
budget.py

Defines the Budget model representing a monthly budget configuration.
"""


class Budget:
    """Represents a monthly budget with an income target and spending limit.

    Attributes:
        month (str): The budget month in YYYY-MM format.
        income_goal (float): Target total income for the month.
        spending_limit (float): Maximum allowed spending for the month.
    """

    def __init__(self, month: str, income_goal: float, spending_limit: float):
        """Initializes a Budget instance.

        Args:
            month (str): Budget month in YYYY-MM format.
            income_goal (float): Target income amount.
            spending_limit (float): Maximum spending allowed.
        """
        self.month = month
        self.income_goal = round(income_goal, 2)
        self.spending_limit = round(spending_limit, 2)

    def to_dict(self) -> dict:
        """Serializes the budget to a dictionary.

        Returns:
            dict: Dictionary representation of the budget.
        """
        return {
            "month": self.month,
            "income_goal": self.income_goal,
            "spending_limit": self.spending_limit,
        }

    def __str__(self) -> str:
        """Returns a formatted string of the budget configuration.

        Returns:
            str: Human-readable budget summary line.
        """
        return (
            f"Month: {self.month} | "
            f"Income Goal: P{self.income_goal:.2f} | "
            f"Spending Limit: P{self.spending_limit:.2f}"
        )
