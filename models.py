# models.py
from datetime import datetime

class Transaction:
    # primary expense class to hold the data for each expense entry
    def __init__(self, number: int, description: str, category: str, 
                 amount: float, date: str):
        self.number = number
        self.description = description
        self.category = category
        self.amount = float(amount)
        self.date = date                        # format: YYYY-MM-DD
        self.t_type = "Expense"                 # Default transaction type Can be changed to "Income"

    @property
    def period_string(self) -> str:
        # Used to group transactions by month
        parts = self.date.split("-")
        if len(parts) == 3:
            year, month, _day = parts
            return f"{year}-{month}"
        return self.date