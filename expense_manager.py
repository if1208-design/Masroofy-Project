from ..models import Expense
from ..dal import DataAccessLayer

class ExpenseManager:

    def __init__(self):
        self.dal = DataAccessLayer()

    def validate_expense(self, amount):
        return amount > 0

    def log_expense(self, amount, category):
        if not self.validate_expense(amount):
            raise ValueError("Invalid amount")

        expense = Expense(amount=amount, category=category)
        self.dal.save_expense(expense)

        return expense