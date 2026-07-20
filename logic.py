# logic.py
from models import Transaction
import re
from typing import Optional

CATEGORY_RULES = {
    "Groceries": {"grocery", "supermarket", "food"},
    "Utilities": {"electricity", "water", "gas"},
    "Dining Out": {"restaurant", "dining", "cafe"},
    "Transportation": {"transportation", "bus", "train", "taxi"},
    "Housing": {"rent", "apartment", "mortgage", "housing"},
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
        # determine category, else, learn new keywords if manually assigned
        if category is None or category == "Auto-Categorize":
            category = self.categorize_description(description, t_type)
        else:
            self.assign_keywords_to_category(description, category) 
        # create transaction and store it
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

    
    # ------------ Category management ------------
    ''' The following section breaks down category management
    in various objects following the single responsibility principle.'''

    def categorize_description(self, description: str, t_type: str) -> str:
        # checks the description against the category rules and returns the appropriate category
        if t_type == "Income":
            return "Salary/Inflow"
        desc_lower = self.extract_keywords(description)
        for category, keywords in self._category_rules.items():
            if desc_lower.intersection(keywords):
                return category
        return "Other"

    def create_category(self, category_name: str, keywords: Optional[set] = None) -> None:
        if category_name not in self._category_rules:
            # if no keywords are created, assign an empty set to the category
            self._category_rules[category_name] = keywords if keywords is not None else set()

    def extract_keywords(self, description: str) -> set:
        # Extract keywords from the description for categorization
        words = re.findall(r'\b[a-z]{3,}\b', description.lower())
        stop_words = {"the", "and", "for", "with", "from", "run", "store", "bill", "payment"}
        return {word for word in words if word not in stop_words}
    
    def add_keywords_to_category(self, category_name: str, keywords: set) -> None:
        # Create the category if it doesn't exist yet, then merge in the keywords
        if category_name not in self._category_rules:
            self._category_rules[category_name] =set()    
        self._category_rules[category_name].update(keywords)

    def assign_keywords_to_category(self, description: str, category_name: str) -> None:
        keywords = self.extract_keywords(description)
        if keywords:
            self.add_keywords_to_category(category_name, keywords)
    ''' end of category management section '''


    # ------------ business functions section ------------
    ''' The following methods are used to calculate totals, 
        summarize by category, and summarize by timeline.'''
    
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

    # Group income vs expense totals by periods.
    def summarize_by_timeline(self) -> dict:
        timeline = {}
        for t in self.transactions.values():
            period = t.period_string
            if period not in timeline:
                timeline[period] = {"Income": 0.0, "Expense": 0.0} 
            timeline[period][t.t_type] += t.amount
        return timeline