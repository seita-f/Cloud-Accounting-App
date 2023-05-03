from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
"""
Index (First page)
"""
def index(request):
    return render(request, 'dashboard.html')
