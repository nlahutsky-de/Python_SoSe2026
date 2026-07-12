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

        # Default transaction type
        self.t_type = "Expense" 

    @property
    def _parsed_date(self):
        try:
            return datetime.strptime(self.date, "%Y-%m-%d")
        except (ValueError, TypeError):
            return datetime.now()

    @property
    def year(self) -> str:
        return str(self._parsed_date.year)

    @property
    def month(self) -> str:
        return f"{self._parsed_date.month:02d}"

    @property
    def day(self) -> str:
        return f"{self._parsed_date.day:02d}"

    @property
    def period_string(self) -> str:
        return self.date