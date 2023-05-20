from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect            # Rediret

# ----- For Login and Logout -----
from .models import UserAccount                  # User Account model
from .forms import AccountForm, AddAccountForm   # User Account Form
from django.views.generic import TemplateView    # Template
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# ----- For Expenses and Category -----
from .models import Expense, Category
from .forms import ExpenseSearchForm, ExpenseForm
from django.views.generic.list import ListView
from .reports import summary_per_category, summary_per_year_month, expense_cost_past_month
from django.db.models import Sum
from django.shortcuts import get_object_or_404

# ----- CRUD -----
from django.views.generic import CreateView, UpdateView, DeleteView
# ----- Login Required -----
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


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
            return render(request, "UserAuthentication/login.html")

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
# def index(request):
#     return render(request, "dashboard.html")


def index(request):
    if request.user.is_authenticated:
        # If user has logged in => Redirect to user page
        return redirect(reverse('expenses:dashboard', args=[request.user.useraccount.random_url]))
    else:
        # If user has not logged in => Redirect to login page
        return render(request, 'dashboard.html', {'login_url': '/login/'})


'''
Expenses
'''
class ExpenseListView(LoginRequiredMixin, ListView):

    # User has not logged in yet
    login_url = '/login/'
    redirect_field_name = 'dashboard'

    # connect to Expense Model
    model = Expense
    paginate_by = 5

    # override to set the filter for a certain user
    def get_queryset(self):
        url_uuid = self.kwargs['url_uuid']
        user_account = get_object_or_404(UserAccount, random_url=url_uuid)
        return self.model.objects.filter(user=user_account.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        form = ExpenseSearchForm(self.request.GET)

        if form.is_valid():
            # name
            name = form.cleaned_data.get('name', '').strip()
            # date
            from_date = form.cleaned_data.get('from_date')
            to_date = form.cleaned_data.get('to_date')
            # multiple categories
            # categories = form.cleaned_data.get('categories')
            # sort choices
            # sort = form.cleaned_data.get('sort')

            # Filter for name
            if name:
                queryset = queryset.filter(name__icontains=name)

            # Filter for date (from and/or to)
            if from_date and to_date:
                queryset = queryset.filter(date__range=(from_date, to_date))
            elif from_date:
                queryset = queryset.filter(date__gte=from_date)
            elif to_date:
                queryset = queryset.filter(date__lte=to_date)

            # Filter for multiple categories
            # if categories:
            #     queryset = queryset.filter(category__in=categories)

        # Filter expenses for the logged-in user
        user_expenses = queryset.filter(user=self.request.user)

        # Total amount spent
        total_amount = user_expenses.aggregate(Sum('amount'))['amount__sum']

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(user_expenses),
            summary_per_year_month=summary_per_year_month(user_expenses),
            summary_past_month=expense_cost_past_month(user_expenses),
            total_amount=total_amount,
            **kwargs)


'''
Category
'''
class CategoryListView(ListView):
    # Connect to Category Model
    model = Category
    paginate_by = 5


'''
Create Expenses
'''
class ExpenseCreateView(LoginRequiredMixin, CreateView):

    # User has not logged in yet
    login_url = '/login/'
    redirect_field_name = 'dashboard'

    model = Expense
    fields = '__all__'
    template_name = 'expenses/create.html'

    def form_valid(self, form):
        expense = form.save(commit=False)
        expense.user = self.request.user
        expense.save()
        return HttpResponseRedirect(reverse('expenses:dashboard', args=[self.request.user.useraccount.random_url]))

    # Override and remove user choice from form
    def get_form(self, form_class=None):
        form = super(ExpenseCreateView, self).get_form(form_class)
        form.fields.pop('user')
        return form


'''
Expense: update and delete
'''
class ExpenseUpdateDeleteView(LoginRequiredMixin, UpdateView):

    # User has not logged in yet
    login_url = '/login/'
    redirect_field_name = 'dashboard'

    model = Expense
    template_name = 'expenses/edit.html'
    form_class = ExpenseForm

    def get_success_url(self):
        # return HttpResponseRedirect(reverse('expenses:dashboard', args=[self.request.user.useraccount.random_url]))
        return reverse('expenses:dashboard', kwargs={'url_uuid': self.request.user.useraccount.random_url})

    def form_valid(self, form):
        expense = form.save(commit=False)
        expense.user = self.request.user
        if self.request.POST.get('action') == 'save':
            expense.save()
        elif self.request.POST.get('action') == 'delete':
            expense.delete()
        return HttpResponseRedirect(self.get_success_url())

    # Not using DeleteView this time
    # def delete(self, request, *args, **kwargs):
    #     expense = self.get_object()
    #     expense.delete()
    #     return HttpResponseRedirect(self.get_success_url())


'''
Category: update and delete
'''
class CategoryCreateDeleteView(LoginRequiredMixin, CreateView):

    # User has not logged in yet
    login_url = '/login/'
    redirect_field_name = 'dashboard'

    model = Category
    template_name = 'category/create-delete.html'
    fields = ['name']


    def get_success_url(self):
        # return HttpResponseRedirect(reverse('expenses:dashboard', args=[self.request.user.useraccount.random_url]))
        return reverse('expenses:dashboard', kwargs={'url_uuid': self.request.user.useraccount.random_url})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        category = form.save(commit=False)
        category.user = self.request.user
        if self.request.POST.get('action') == 'add':
            category.save()
        elif self.request.POST.get('action') == 'delete':
            category.delete()
        return HttpResponseRedirect(self.get_success_url())

