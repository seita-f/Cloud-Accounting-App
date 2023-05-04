from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect            # Rediret

# For Login and Logout
from .models import UserAccount                  # User Account model
from django.views.generic import TemplateView    # Template
from .forms import AccountForm, AddAccountForm   # User Account Form
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# For Expenses and Category
from django.views.generic.list import ListView
# from .forms import ExpenseSearchForm
# from .models import Expense, Category
from .reports import summary_per_category, summary_per_year_month

from django.db.models import Sum

# User Register
class AccountRegistration(TemplateView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.params = {
            "AccountCreate": False,
            "account_form": AccountForm(),
            "add_account_form": AddAccountForm(),
        }

    # Get
    def get(self, request, *args, **kwargs):
        self.params["account_form"] = AccountForm()
        self.params["AccountCreate"] = False
        return render(request, "UserAuthentication/register.html", context=self.params)

    # Post
    def post(self, request, *args, **kwargs):
        self.params["account_form"] = AccountForm(data=request.POST)
        self.params["add_account_form"] = AddAccountForm(data=request.POST)

        # Check if given data is valid
        if self.params["account_form"].is_valid():
            # Save account info in DB
            account = self.params["account_form"].save()
            # Hash password
            account.set_password(account.password)
            # Update hash password
            account.save()

            add_account = self.params["add_account_form"].save(commit=False)
            # AccountForm & AddAccountForm 1vs1
            add_account.user = account
            # save the model
            add_account.save()

            # Upgrade user account creation
            self.params["AccountCreate"] = True

        else:
            # If the form is not valid
            print(self.params["account_form"].errors)

        return render(request, "UserAuthentication/register.html", context=self.params)

# Log In
def Login(request):
    # POST
    if request.method == 'POST':
        # Get email and password from form
        userid = request.POST.get('userid')
        password = request.POST.get('password')

        # Django Authentication function
        user = authenticate(username=userid, password=password)

        # Check if it is valid user
        if user:
            # Check activate of user
            if user.is_active:
                # Login
                login(request, user)

                # Get the associated UserAccount object
                user_account = UserAccount.objects.get(user=user)

                # Valid account, then go to homepage with unique url
                return HttpResponseRedirect(reverse('expenses:dashboard', args=[user_account.random_url]))

            else:
                # Invalid account
                return HttpResponse("Invalid Account")
        # Fail user authentication
        else:
            return HttpResponse("Email or Password is wrong :(")
    # GET
    else:
        return render(request, 'UserAuthentication/login.html')

# Log out
@login_required
def Logout(request):
    logout(request)
    # Redirect to the login page
    return redirect('login')


# Home page before user log in
def index(request):
    return render(request, "index.html")


# Home Page after log in
@login_required
def dashboard(request, url_uuid):
    try:
        user_account = UserAccount.objects.get(random_url=url_uuid)
    except UserAccount.DoesNotExist:
        # URL is not valid
        return HttpResponseNotFound("Page not found")

    # params = {"userid": request.user, }
    params = {"user_account": user_account }
    return render(request, "dashboard.html", context=params)


# '''
# Expenses
# '''
# class ExpenseListView(ListView):
#
#     # connect to Expense Model
#     model = Expense
#     paginate_by = 5
#
#     # override to set the filter for a certain user
#     def get_queryset(self):
#         return self.model.objects.filter(
#             username=self.request.user,
#         )
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         queryset = object_list if object_list is not None else self.object_list
#         form = ExpenseSearchForm(self.request.GET)
#
#         if form.is_valid():
#             # name
#             name = form.cleaned_data.get('name', '').strip()
#             # date
#             from_date = form.cleaned_data.get('from_date')
#             to_date = form.cleaned_data.get('to_date')
#             # multiple categories
#             categories = form.cleaned_data.get('categories')
#             # sort choices
#             # sort = form.cleaned_data.get('sort')
#
#             # Filter for name
#             if name:
#                 queryset = queryset.filter(name__icontains=name)
#
#             # Filter for date (from and/or to)
#             if from_date and to_date:
#                 queryset = queryset.filter(date__range=(from_date, to_date))
#             elif from_date:
#                 queryset = queryset.filter(date__gte=from_date)
#             elif to_date:
#                 queryset = queryset.filter(date__lte=to_date)
#
#             # Filter for multiple categories
#             if categories:
#                 queryset = queryset.filter(category__in=categories)
#
#         # Total amount spent
#         amount_dict = Expense.objects.all().aggregate(Sum('amount'))
#         total_amount = amount_dict['amount__sum']
#
#         return super().get_context_data(
#             form=form,
#             object_list=queryset,
#             summary_per_category=summary_per_category(queryset),
#             summary_per_year_month=summary_per_year_month(queryset),
#             total_amount=total_amount,
#             **kwargs)
#
#
# '''
# Category
# '''
# class CategoryListView(ListView):
#     # Connect to Category Model
#     model = Category
#     paginate_by = 5
#
