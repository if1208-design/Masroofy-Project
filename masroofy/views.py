from django.shortcuts import render, redirect
from .models import Login ,Sign
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

            result = manager.add_expense(amount, category)

            warning = result["warning"]

            if warning:
                request.session["warning"] = warning

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

    warning = request.session.pop("warning", None)

    return render(request, "dashboard.html", {
        "daily": budget.daily_limit,
        "spent": budget.spent,
        "remaining": remaining,
        "warning": warning
    })

def reset_budget(request):
    Budget.objects.all().delete()
    return redirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        data = Login( username=username, password=password)
        data.save()


    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = Sign(
            username=username,
            email=email,
            password=password
        )
        user.save()
 
    return render(request, "signup.html")