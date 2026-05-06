from ..models import Budget

class ApplicationLogicEngine:

    def process_transaction(self, amount):
        budget = Budget.objects.first()

        if budget:
            budget.remaining -= amount
            budget.save()