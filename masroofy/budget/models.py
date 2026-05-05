import datetime
from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    monthly_income = models.FloatField()

    def __str__(self):
        return self.name
    
    def get_total_expenses(self):
        return sum(expense.amount for expense in self.expense_set.all())
    
    def remaining_budget(self):
        return self.monthly_income - self.get_total_expenses()
    
    def remaining_days_in_month(self):
        today = datetime.date.today()
        
        if today.month == 12:
            next_month = datetime.date(today.year+ 1, 1, 1)
        else:
            next_month = datetime.date(today.year, today.month + 1, 1)

        last_day = next_month - datetime.timedelta(days=1)
        return (last_day - today).days + 1
        
    def safe_daily_limit(self):
        days = self.remaining_days_in_month()

        if days <= 0:
            return 0
        return self.remaining_budget() / days
    
    # Adjust the daily limit based on actual spending today.
    def adjusted_daily_limit(self):
        today = datetime.date.today()
        
        remaining_budget = self.remaining_budget()
        remaining_days = self.remaining_days_in_month()

        if remaining_days == 0:
            return 0

        return remaining_budget / remaining_days

class Expense(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.amount} on {self.date}"
    