# models.py
from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    name = models.CharField(max_length=140)
    date_of_expense = models.DateField()
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    description = models.TextField()
    amount = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name