from django.urls import path
from . import views

urlpatterns = [
    path('expenses/', views.get_expenses),
    path('add/', views.add_expense),
    path('delete/<int:expense_id>/', views.delete_expense),
    path('dashboard/', views.dashboard),
]