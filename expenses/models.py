from django.db import models

# Create your models here.

class Expense(models.Model):
    amount = models.FloatField()
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class Budget(models.Model):
    total = models.FloatField()
    remaining = models.FloatField()
