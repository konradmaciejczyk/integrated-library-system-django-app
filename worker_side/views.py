from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import  UserRegisterForm

def home(request):
    context = {'title': 'Work desktop - Online Library Catalog for librarian'}
    return render(request, 'worker_side/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('worker_side-home')
    else:
        form = UserRegisterForm()

    return render(request, 'worker_side/register.html', {'form': form})

def log_in(request):
    return render(request, 'worker_side/log_in.html')


