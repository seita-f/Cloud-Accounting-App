from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser

# User
from django.contrib.auth.models import User
import uuid   # generate random num for URL

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


'''
Expenses
'''
