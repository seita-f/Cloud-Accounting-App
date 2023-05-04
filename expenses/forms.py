from django import forms
from django.contrib.auth.models import User
from .models import UserAccount
# from .models import Expense, Category

'''
User 
'''
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

#
# '''
# Expenses
# '''
# class ExpenseSearchForm(forms.ModelForm):
#
#     # Widgets for searching date
#     from_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
#     to_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
#
#     # Widgets for multiple categories
#     categories = forms.ModelMultipleChoiceField(
#         queryset=Category.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )
#
#     # Widgets for sort choices
#     # sort_choices = (
#     #     ('category_asc', 'Category (Ascending)'),
#     #     ('category_desc', 'Category (Descending)'),
#     #     ('date_asc', 'Date (Ascending)'),
#     #     ('date_desc', 'Date (Descending)'),
#     # )
#     # sort = forms.ChoiceField(choices=sort_choices, required=False)
#
#     class Meta:
#         model = Expense
#         fields = ('name', 'from_date', 'to_date', 'categories',)  # add fields
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['name'].required = False
