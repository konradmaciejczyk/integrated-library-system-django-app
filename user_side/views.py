from django.shortcuts import render
from .models import Readers

def home(request):
    return render(request, "user_side/home.html")

def search(request):
    context = {
        'readers': Readers.objects.all()
    }
    return render(request, "user_side/search.html", context)
