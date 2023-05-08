from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser

# User
from django.contrib.auth.models import User
import uuid   # generate random num for URL

# Category & Expenses
import datetime
from django.db.models import Sum  # Sum expenses


'''
User
'''
class UserAccount(models.Model):

    # instance
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # add filed
    random_url = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)   # Unique URL for a user

    def __str__(self):
        return self.user.username

    def generate_unique_url(self):
        url_uuid = uuid.uuid4()
        self.random_url = url_uuid
        self.save()
        return url_uuid


# One-to-Many relation (Category - Expenses)

'''
Category
'''

class Category(models.Model):

    # I will let category be an independent model
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)   # ascending order

    def __str__(self):
        return f'{self.name}'

    @property
    def total_expense_amount(self):
        return self.expense_set.aggregate(Sum('amount'))['amount__sum'] or 0


'''
Expenses
'''
class Expense(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # set User as a ForeignKey
    # models.PROTECT => not remove category when expense is removed
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)

    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    date = models.DateField(default=datetime.date.today, db_index=True)

    class Meta:
        ordering = ('-date', '-pk')   # descending order

    def __str__(self):
        return f'{self.date} {self.name} {self.amount}'
