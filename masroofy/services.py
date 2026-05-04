from .models import Budget


class LimitCalculator:
    def calculate_daily_limit(self, allowance, days):
        return allowance / days


from .models import Budget


class BudgetManager:
    def initialize_budget(self, user_id, allowance, days):
        daily_limit = allowance / days

        budget = Budget.objects.create(
            user_id=user_id,
            allowance=allowance,
            days=days,
            daily_limit=daily_limit
        )

        return budget
    

class ExpenseManager:
    def add_expense(self, amount, category):
        if amount <= 0 or not category:
            raise ValueError("Invalid input")

        budget = Budget.objects.first()

        budget.spent += amount
        budget.save()

        return budget