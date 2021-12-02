from time import time
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import  ClientRegistrationForm
from datetime import datetime, timedelta
from user_side.models import Citizenship

def home(request):
    return render(request, 'worker_side/home.html')

def register_user(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account successful created!')
            return redirect('worker_side-home')
    else:
        form = ClientRegistrationForm()

    five_years_ago = (datetime.today() - timedelta(6*365))
    context = {
        'form': form,
        'max_date': five_years_ago.date().strftime("%Y-%m-%d"),
        'citizenships': Citizenship.objects.all()
    }
    
    return render(request, 'worker_side/register_user.html', context)

def log_in(request):
    return render(request, 'worker_side/log_in.html')


