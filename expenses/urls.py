from django.urls import path
from . import views
from .views import ExpenseListView, ExpenseCreateView, ExpenseUpdateDeleteView, CategoryCreateDeleteView
from .models import Expense
from django.urls import reverse

app_name = 'expenses'

urlpatterns = [

    # First page
    path('', views.index, name='index'),

    # path('', ExpenseListView.as_view(template_name='dashboard.html'), name='dashboard'),

    # Register page
    path('register', views.AccountRegistration.as_view(), name='register'),

    # Login Page
    path('login', views.Login, name='login'),

    # Logout page
    path('logout', views.Logout, name="logout"),

    # Dashboard (Expenses ListView)
    path('expense/list/<uuid:url_uuid>',
         ExpenseListView.as_view(
             template_name='dashboard.html'
         ),
         name='dashboard'),

    # Create Expenses
    path('expense/create/',
        ExpenseCreateView.as_view(),
        name='expense-create'),

    # Update / Delete Expenses
    path('expense/list/<uuid:url_uuid>/<int:pk>/',
         ExpenseUpdateDeleteView.as_view(
        ),
        name='expense-edit'),

    # Category Create and Delete
    path('category/list/<uuid:url_uuid>',
         CategoryCreateDeleteView.as_view(
         ),
         name='category-edit'),

    # Analytics
    path('expense/analytics/<uuid:url_uuid>',
         ExpenseListView.as_view(
            template_name="analytics.html"),
         name="analytics"),

]
