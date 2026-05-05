from django.urls import path
from .views import dashboard, add_expense

urlpatterns = [
    path('', dashboard, name = 'dashboard'), # This will be the main page showing the dashboard
    path('add-expense/', add_expense, name='add_expense'), # This will be the page to add a new expense  
]