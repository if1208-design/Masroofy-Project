from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),      
    path('init', views.init_budget),
    path('add-expense', views.add_expense),
    path('reset', views.reset_budget),
    path('login/', views.login_view),
    path("signup/", views.signup, name="signup"),
]

