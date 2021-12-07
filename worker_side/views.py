from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import  ClientRegistrationForm
from datetime import datetime, timedelta
from accounts.models import Citizenship



def home(request):
    return render(request, 'worker_side/home.html')

def register_user(request):
    password = None
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            password = form.save()
            messages.success(request, f'Account created successfully! {password}')
            return redirect('worker_side-home')
        else:
            messages.error(request, f'Form filled with invalid informations!')
            return redirect('worker_side-register_user')
    else:
        five_years_ago = (datetime.today() - timedelta(6*365))
        context = {
            'max_date': five_years_ago.date().strftime("%Y-%m-%d"),
            'citizenships': Citizenship.objects.all()
        }
        
        return render(request, 'worker_side/register_user.html', context)

def add_item(request):
    return render(request, 'worker_side/add_item.html')




