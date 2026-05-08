from django.db import models

class Budget(models.Model):
    user_id = models.IntegerField()
    allowance = models.FloatField()
    days = models.IntegerField()
    daily_limit = models.FloatField()
    spent = models.FloatField(default=0)


class SavingGoal(models.Model):
    target_amount = models.FloatField()
    current_amount = models.FloatField(default=0)

class Login(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=30)

class Sign(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)

class Expense(models.Model):
    amount = models.FloatField()
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category

# Create your models here.