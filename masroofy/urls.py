from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
   path("dashboard/", views.dashboard, name="dashboard"),    
    path('init/', views.init_budget, name='init_budget'),
    path('add-expense', views.add_expense),
    path('reset', views.reset_budget),
    path('login/', views.login_view, name='login'),
    path("signup/", views.signup, name="signup"),
    path('reports/', views.reports, name='reports'),
    path('goal/', views.saving_goal, name='goal'),
    path('history/', views.history, name='history'),
    path('pieChart/',views.pie),
    path('logout/', views.logout_view, name='logout'),

    path('delete/<int:id>/', views.delete_expense, name='delete_expense')
]