from django.db import models

class Budget(models.Model):
    user_id = models.IntegerField()
    allowance = models.FloatField()
    days = models.IntegerField()
    daily_limit = models.FloatField()
    spent = models.FloatField(default=0)


# Create your models here.
