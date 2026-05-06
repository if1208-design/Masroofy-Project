from .models import Expense

class DataAccessLayer:

    def get_all_expenses(self):
        return Expense.objects.all()

    def save_expense(self, expense):
        expense.save()

    def delete_expense(self, expense_id):
        Expense.objects.filter(id=expense_id).delete()