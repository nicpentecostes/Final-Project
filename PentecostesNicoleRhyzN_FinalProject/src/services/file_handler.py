"""
file_handler.py

Handles reading and writing budget planner data to a JSON file.
Uses context managers for safe file I/O operations.
"""

import json
import os


class FileHandler:
    """Manages persistence of budget and transaction data to a JSON file.

    Attributes:
        FILE_PATH (str): Relative path to the JSON data file.
    """

    FILE_PATH = os.path.join("src", "data", "budget_data.json")

    @staticmethod
    def load_data() -> dict:
        """Loads all planner data from the JSON file.

        Returns:
            dict: A dictionary with 'budgets' and 'transactions' keys,
                  or default empty structure if file is missing or corrupt.
        """
        default = {"budgets": [], "transactions": []}

        if not os.path.exists(FileHandler.FILE_PATH):
            return default

        try:
            with open(FileHandler.FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    return data
                return default
        except (json.JSONDecodeError, OSError):
            return default

    @staticmethod
    def save_data(data: dict) -> None:
        """Saves all planner data to the JSON file.

        Args:
            data (dict): Dictionary containing 'budgets' and 'transactions'.
        """
        os.makedirs(os.path.dirname(FileHandler.FILE_PATH), exist_ok=True)

        with open(FileHandler.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
