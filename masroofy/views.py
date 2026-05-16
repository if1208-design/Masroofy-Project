from django.shortcuts import render, redirect
from .models import Budget ,Expense
from .services import ExpenseManager
from .services import BudgetManager
from .models import SavingGoal
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from .models import Budget, SavingGoal

def init_budget(request):
    if request.method == "POST":
        allowance = float(request.POST.get("allowance"))
        days = int(request.POST.get("days"))

        manager = BudgetManager()
        budget = manager.initialize_budget(1, allowance, days)

        print("SAVED:", budget)   # 👈 مهم

        return redirect('/')

    return render(request, "init_budget.html")

def add_expense(request):

    if request.method == "POST":

        amount = float(request.POST.get("amount"))
        category = request.POST.get("category")

        try:

            manager = ExpenseManager()

            result = manager.add_expense(amount, category)

            Expense.objects.create(
                amount=amount,
                category=category
            )

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
    if not request.user.is_authenticated:
        return redirect('login')

    budget = Budget.objects.last()

    if not budget:
        return redirect('init_budget')

    remaining = budget.allowance - budget.spent

    return render(request, "dashboard.html", {
        "daily": budget.daily_limit,
        "spent": budget.spent,
        "remaining": remaining
    })



def reports(request):
    budget = Budget.objects.last()

    if not budget:
        return redirect('/')

    spent_percentage = (budget.spent / budget.allowance) * 100

    return render(request, "reports.html", {
        "allowance": budget.allowance,
        "spent": budget.spent,
        "remaining": budget.allowance - budget.spent,
        "percentage": spent_percentage
    })




# def reset_budget(request):
#     Budget.objects.all().delete()
#     return redirect('dashboard')
def reset_budget(request):
    Budget.objects.all().delete()
    SavingGoal.objects.all().delete()

    return redirect('dashboard')

from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, "login.html", {
                "error": "Invalid credentials"
            })

    return render(request, "login.html")

from django.contrib.auth.models import User
from django.contrib.auth import login

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect('dashboard')

    return render(request, "signup.html")
  

def saving_goal(request):

    goal = SavingGoal.objects.last()

    if request.method == "POST":

        target = float(request.POST.get("target"))

        if goal:
            goal.target_amount = target
            goal.save()
        else:
            SavingGoal.objects.create(
                target_amount=target
            )

        return redirect('/goal')

    if goal:
        budget = Budget.objects.last()

        current_saving = budget.allowance - budget.spent

        goal.current_amount = current_saving
        goal.save()

        percentage = (
            goal.current_amount / goal.target_amount
        ) * 100

    else:
        percentage = 0

    return render(request, "goal.html", {
        "goal": goal,
        "percentage": percentage
    })


def history(request):
    expenses = Expense.objects.all()
    return render(request, "history.html", {
        "expenses": expenses
    })



def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id)

    if request.method == "POST":
        budget = Budget.objects.last()

        budget.spent -= expense.amount
        budget.save()

        expense.delete()

    return redirect('history')

def pie(request):
    data = Expense.objects.values('category').annotate(total=Sum('amount'))

    totals = {}
    percentages = {}

    total_sum = sum(item['total'] for item in data)

    for item in data:
        category = item['category']
        amount = item['total']

        totals[category] = amount

        if total_sum != 0:
            percentages[category] = (amount / total_sum) * 100

    return render(request, "pieChart.html", {
        "totals": totals,
        "percentages": percentages
    })

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, "home.html")

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')

    return render(request, "logout.html")

def logout_view(request):
    logout(request)
    return redirect('home')