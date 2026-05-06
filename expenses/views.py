from django.shortcuts import render, redirect
from django.http import JsonResponse

from .dal import DataAccessLayer
from .services.expense_manager import ExpenseManager
from .services.logic_engine import ApplicationLogicEngine
from .services.dashboard_service import DashboardService


def home(request):
    return redirect('expenses/')


def get_expenses(request):
    dal = DataAccessLayer()
    expenses = dal.get_all_expenses()

    return render(request, 'expenses/history.html', {
        'expenses': expenses
    })



def add_expense(request):
    if request.method == "POST":
        try:
            amount = float(request.POST.get("amount", 0))
            category = request.POST.get("category", "")

            manager = ExpenseManager()
            engine = ApplicationLogicEngine()

        
            manager.log_expense(amount, category)

            engine.process_transaction(amount)

            return redirect('/expenses/')

        except Exception:
            return render(request, 'expenses/add.html', {
                "error": "Invalid input"
            })

    return render(request, 'expenses/add.html')


def delete_expense(request, expense_id):
    dal = DataAccessLayer()
    dal.delete_expense(expense_id)

    return redirect('/expenses/')


def dashboard(request):
    service = DashboardService()
    report = service.generate_report()

    if not report["totals"]:
        return render(request, 'expenses/dashboard.html', {
            "message": "No expenses yet"
        })

    return render(request, 'expenses/dashboard.html', report)