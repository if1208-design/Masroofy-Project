from django.shortcuts import render, redirect
from .models import Budget
from .services import BudgetManager
def init_budget(request):
    if request.method == "POST":
        allowance = float(request.POST.get("allowance"))
        days = int(request.POST.get("days"))

        manager = BudgetManager()
        budget = manager.initialize_budget(1, allowance, days)

        print("SAVED:", budget)   # 👈 مهم

        return redirect('/')

    return render(request, "init_budget.html")

from .services import ExpenseManager

def add_expense(request):
    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        category = request.POST.get("category")

        try:
            manager = ExpenseManager()
            manager.add_expense(amount, category)
            return redirect('/')
        except:
            return render(request, "add_expense.html", {
                "error": "Invalid input"
            })

    return render(request, "add_expense.html")

def dashboard(request):
    budget = Budget.objects.last()

    if not budget:
        return render(request, "init_budget.html")

    remaining = budget.allowance - budget.spent

    return render(request, "dashboard.html", {
        "daily": budget.daily_limit,
        "spent": budget.spent,
        "remaining": remaining
    })
def reset_budget(request):
    Budget.objects.all().delete()
    return redirect('/')