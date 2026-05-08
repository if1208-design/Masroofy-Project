from django.shortcuts import render, redirect
from .models import Login ,Sign
from .models import Budget 
from .services import BudgetManager
from .models import SavingGoal

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


        

from .models import Expense

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

from django.shortcuts import get_object_or_404


def history(request):

    expenses = Expense.objects.all()

    return render(request, "history.html", {
        "expenses": expenses
    })


def edit_expense(request, id):

    expense = get_object_or_404(Expense, id=id)

    if request.method == "POST":

        new_amount = float(request.POST.get("amount"))
        new_category = request.POST.get("category")

        budget = Budget.objects.last()

        old_amount = expense.amount

        difference = new_amount - old_amount

        budget.spent += difference

        budget.daily_limit = (
            budget.allowance - budget.spent
        ) / budget.days

        budget.save()

        expense.amount = new_amount
        expense.category = new_category
        expense.save()

        return redirect('/history')

    return render(request, "edit_expense.html", {
        "expense": expense
    })



from .models import Expense
from django.shortcuts import get_object_or_404


def history(request):

    expenses = Expense.objects.all()

    return render(request, "history.html", {
        "expenses": expenses
    })


def edit_expense(request, id):

    expense = get_object_or_404(Expense, id=id)

    if request.method == "POST":

        new_amount = float(request.POST.get("amount"))
        new_category = request.POST.get("category")

        manager = ExpenseManager()

        manager.edit_expense(
            expense.amount,
            new_amount
        )

        expense.amount = new_amount
        expense.category = new_category

        expense.save()

        return redirect('/history')

    return render(request, "edit_expense.html", {
        "expense": expense
    })


def delete_expense(request, id):

    expense = get_object_or_404(Expense, id=id)

    if request.method == "POST":

        manager = ExpenseManager()

        manager.delete_expense(
            expense.amount
        )

        expense.delete()

        return redirect('/history')

    return render(request, "delete_expense.html", {
        "expense": expense
    })

from .models import Expense
from .services import get_category_breakdown

def pie(request):
    expenses = Expense.objects.all()

    breakdown = get_category_breakdown(expenses)

    return render(request, "dashboard.html", {
        "breakdown": breakdown
    })