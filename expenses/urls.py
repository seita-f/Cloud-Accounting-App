from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [

    path('', views.index, name='index'),

    # dashboard after user login
    path('dashboard/<uuid:url_uuid>', views.dashboard, name='dashboard'),  # unique URL

    # Register page
    path('register', views.AccountRegistration.as_view(), name='register'),

    # Login Page
    path('login', views.Login, name='login'),

    # Logout page
    path('logout', views.Logout, name="logout"),

    # Feedback Page
    # path('feedback/<uuid:url_uuid>', views.FeedBack_page, name='feedback'),  # unique URL

]