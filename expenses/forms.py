from django import forms
from django.contrib.auth.models import User
from .models import UserAccount

# Form class
class AccountForm(forms.ModelForm):
    # form for password (not visible)
    password = forms.CharField(widget=forms.PasswordInput(), label="password")

    class Meta():
        # Uer
        model = User
        # Fields
        fields = ('username', 'email', 'password')
        # Name for fields
        labels = {'username': "username", 'email': "email"}


class AddAccountForm(forms.ModelForm):
    class Meta():
        # Model class
        model = UserAccount
        fields = ()
        labels = {}
