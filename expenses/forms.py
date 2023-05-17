from django import forms
from django.contrib.auth.models import User
from .models import UserAccount
from .models import Expense, Category

'''
User 
'''
class AccountForm(forms.ModelForm):
    # form for password (not visible)
    # password = forms.CharField(widget=forms.PasswordInput(), label="password")

    # Form for password (not visible)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Password")
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label="Email")
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Username")

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


'''
Expenses
'''
class ExpenseSearchForm(forms.ModelForm):

    # Widgets for searching date
    from_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Expense
        fields = ('name', 'from_date', 'to_date',)  # add fields

    def __init__(self, *args, **kwargs):  # pass the login user
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False

# # Widgets for multiple categories
    # categories = forms.ModelMultipleChoiceField(
    #     queryset=Category.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False
    # )

    # Widgets for sort choices
    # sort_choices = (
    #     ('category_asc', 'Category (Ascending)'),
    #     ('category_desc', 'Category (Descending)'),
    #     ('date_asc', 'Date (Ascending)'),
    #     ('date_desc', 'Date (Descending)'),
    # )
    # sort = forms.ChoiceField(choices=sort_choices, required=False)

'''
Expenses Form
'''
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ['user']  # exclude the user field from the form
