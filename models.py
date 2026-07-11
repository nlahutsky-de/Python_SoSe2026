from datetime import datetime

class Transaction:
     # primary expense class to hold the data for each expense entry
    def __init__(self, number: int, description: str, category: str, amount: float, year: str, month: str):
        self.number = number
        self.description = description
        self.category = category
        self.amount = float(amount)
        self.year = year
        self.month = month

         # Default transaction type
        self.t_type = "Expense" 

    @property
    def period_string(self) -> str:
    # Returns the year and month (YYYY-MM)
        return f"{self.year}-{self.month}"