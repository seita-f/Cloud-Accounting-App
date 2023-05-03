from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    # Home path
    path('', views.index, name='index'),
]