from django.shortcuts import render
from django.contrib.auth.decorators import login_required
#from .models import Clients

def home(request):
    return render(request, "user_side/home.html")

def search(request):
    context = {
        'title': "Search results for ... - Online Library Catalog"
    }
    
    return render(request, "user_side/search.html", context)

def log_in(request):
    return render(request, "user_side/log_in.html")

@login_required
def profile(request):
    return render(request, "user_side/profile.html")