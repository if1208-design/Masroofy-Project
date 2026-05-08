
from .models import Budget


class LimitCalculator:
    def calculate_daily_limit(self, allowance, days):
        return allowance / days


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

        budget.daily_limit = (
            budget.allowance - budget.spent
        ) / budget.days

        budget.save()

        threshold = budget.allowance * 0.8

        if budget.spent >= threshold:

            return {
                "warning": "Warning: You have used 80% of your allowance.",
                "budget": budget
            }

        return {
            "warning": None,
            "budget": budget
        }


    def edit_expense(self, old_amount, new_amount):

        budget = Budget.objects.first()

        difference = new_amount - old_amount

        budget.spent += difference

        budget.daily_limit = (
            budget.allowance - budget.spent
        ) / budget.days

        budget.save()

        return budget


    def delete_expense(self, amount):

        budget = Budget.objects.first()

        budget.spent -= amount

        budget.daily_limit = (
            budget.allowance - budget.spent
        ) / budget.days

        budget.save()

        return budget
    
from collections import defaultdict

def get_category_breakdown(expenses):
    if not expenses:
        return {}

    totals = defaultdict(float)
    total_spent = 0

    for e in expenses:
        totals[e.category] += e.amount
        total_spent += e.amount

    if total_spent == 0:
        return {}

    result = {}

    for category, amount in totals.items():
        result[category] = (amount / total_spent) * 100

    return result