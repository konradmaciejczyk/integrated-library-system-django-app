from django.shortcuts import render
from .models import Readers

def home(request):
    context = {
        'title': 'Online Library Catalog'
    }
    return render(request, "user_side/home.html", context)

def search(request):
    context = {
        'title': "Search results for ... - Online Library Catalog",
        'readers': Readers.objects.all()
    }
    return render(request, "user_side/search.html", context)

def log_in(request):
    return render(request, "user_side/log_in.html", {'title': 'Sign in to Online Library Catalog'})
