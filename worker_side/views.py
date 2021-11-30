from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import  ClientRegistrationForm

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

    return render(request, 'worker_side/register_user.html', {'form': form})

def log_in(request):
    return render(request, 'worker_side/log_in.html')


