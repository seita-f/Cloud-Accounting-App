from django.urls import path
from . import views
from .views import ExpenseListView, ExpenseCreateView, ExpenseUpdateDeleteView
from .models import Expense
from django.urls import reverse

app_name = 'expenses'

urlpatterns = [

    path('', views.index, name='index'),

    # dashboard after user login
    # path('dashboard/<uuid:url_uuid>', views.dashboard, name='dashboard'),  # unique URL

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
    path('expense/list/<uuid:url_uuid>/<int:pk>/', ExpenseUpdateDeleteView.as_view(

        ),
        name='expense-edit'),

]
