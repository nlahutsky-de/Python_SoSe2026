# finance_tracker.py
from models import Transaction

CATEGORY_RULES = {
    "Groceries": {"grocery", "supermarket", "food"},
    "Utilities": {"electricity", "water", "gas"},
    "Dining Out": {"restaurant", "dining", "cafe"},
    "Transportation": {"transportation", "bus", "train", "taxi"},
    "Salary/Inflow": {"salary", "paycheck", "bonus", "dividend"}
}

class ExpenseManager:

    def __init__(self):
        self.transactions = {}
        self._next_number = 1
        self._category_rules = dict(CATEGORY_RULES)
  

    # Add a new income or expense    
    def add_transaction(self, t_type: str, description: str, amount: float, 
                        date: str, category: str) -> Transaction:
        
        if category is None or category == "Auto-Categorize":
            category = self.categorize_description(description, t_type)
            
        if category not in self._category_rules:
            self._category_rules[category] = set()

        transaction = Transaction(self._next_number, description, category, amount, date)

        # Save whether it is income or expense
        transaction.t_type = t_type 
        
        self.transactions[self._next_number] = transaction
        self._next_number += 1
        return transaction

    def delete_transaction(self, number: int) -> bool:
        if number in self.transactions:
            del self.transactions[number]
            return True
        return False

    def update_transaction(self, number: int, new_type: str, new_description: str, new_amount: float, 
                           new_date: str, new_category: str) -> bool:
        if number in self.transactions:
            t = self.transactions[number]
            t.t_type = new_type
            t.description = new_description
            t.amount = float(new_amount)
            t.date = new_date
            t.category = new_category
            return True
        return False

    def categorize_description(self, description: str, t_type: str) -> str:
        # checks the description against the category rules and returns the appropriate category
        if t_type == "Income":
            return "Salary/Inflow"
        
        desc_lower = description.lower()

        for category, keywords in self._category_rules.items():
            if any(keyword in desc_lower for keyword in keywords):
                return category
            
        return "Other"

    # Calculate total income, expenses, and savings.
    def calculate_totals(self) -> dict:

        totals = {
            "Income": 0.0, 
            "Expense": 0.0, 
            "Savings": 0.0
        }

        for t in self.transactions.values():
            if t.t_type == "Income":
                totals["Income"] += t.amount
            else:
                totals["Expense"] += t.amount

        totals["Savings"] = totals["Income"] - totals["Expense"]
        return totals

    # Add up expenses for each category
    def summarize_by_category(self) -> dict:
        summary = {}
        for t in self.transactions.values():
            if t.t_type == "Expense":
                if t.category not in summary:
                    summary[t.category] = 0.0
                summary[t.category] += t.amount
        return summary

    def highest_spending_category(self) -> str:
        summary = self.summarize_by_category()
        if not summary:
            return "None"
        max_value = max(summary.values())
        highest_cats = [cat for cat, amt in summary.items() if amt == max_value]
        return ", ".join(highest_cats)

    # Group income vs expense totals by month periods.
    def summarize_by_timeline(self) -> dict:
        timeline = {}

        for t in self.transactions.values():
            period = t.period_string

            if period not in timeline:
                timeline[period] = {"Income": 0.0, "Expense": 0.0} 
            timeline[period][t.t_type] += t.amount
        return timeline