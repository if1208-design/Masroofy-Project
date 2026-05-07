import datetime

from django.shortcuts import render, redirect
from .models import Student
from .forms import ExpenseForm

# Create your views here.
def dashboard(request):
    student = Student.objects.first()  # For simplicity, we use the first student

    if not student:
        context = {
        'remaining_budget': 0,
        'remaining_days': 0,
        'safe_daily_limit': 0,
        'adjusted_daily_limit': 0,
        'today_spending': 0,
        'warning': None,
        }
        return render(request, 'dashboard.html', context)
    
    today = datetime.date.today()

    today_expenses = student.expense_set.filter(date=today)
    today_spending = sum(e.amount for e in today_expenses)

    safe_daily_limit = student.safe_daily_limit()
    remaining_budget = student.remaining_budget()
    remaining_days_in_month = student.remaining_days_in_month()
    adjusted_daily_limit = student.adjusted_daily_limit()

    warning = None
    if today_spending > safe_daily_limit:
        warning = "⚠ You exceeded today's safe limit!"

    context = {
        "remaining_budget": remaining_budget,
        "remaining_days": remaining_days_in_month,
        "safe_daily_limit": safe_daily_limit,
        "adjusted_daily_limit": adjusted_daily_limit,
        "today_spending": today_spending,
        "warning": warning,
    }
    return render(request, "dashboard.html", context)

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()

    return render(request, 'add_expense.html', {'form': form})