from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import  AddBookForm, ClientRegistrationForm, AddMovieForm, AddSoundRecordingForm
from datetime import datetime, timedelta
from accounts.models import Citizenship
from worker_side.models import Author, Director, Publisher

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

def add_book(request):
    context = {'authors': Author.objects.all(),
               'publishers': Publisher.objects.all(),
               'form': AddBookForm()}

    if request.method == 'POST':
        print("CO PRZYSZŁO", request.POST)
        form = AddBookForm(request.POST, request.FILES)
        if form.is_valid():
            data_to_summary = form.save()
            return render(request, template_name='worker_side/item_summary.html', context=data_to_summary)
        else:
            print("BŁĘDY: ", form.errors, "\nDATA: ", form.cleaned_data)
            messages.error(request, f'Form filled with invalid informations!')
            return redirect('worker_side-add_book')
    else:
        form = AddBookForm(request.POST, request.FILES)
        return render(request, template_name='worker_side/add_book.html', context=context)

def add_movie(request):
    context = {'directors': Director.objects.all(),
               'publishers': Publisher.objects.all(),
               'form': AddMovieForm()}

    if request.method == 'POST':
        print("CO PRZYSZŁO", request.POST)
        form = AddMovieForm(request.POST, request.FILES)
        if form.is_valid():
            data_to_summary = form.save()
            return render(request, template_name='worker_side/item_summary.html', context=data_to_summary)
        else:
            print("BŁĘDY: ", form.errors, "\nDATA: ", form.cleaned_data)
            messages.error(request, f'Form filled with invalid informations!')
            return redirect('worker_side-add_movie')
    else:
        form = AddMovieForm(request.POST, request.FILES)
        return render(request, template_name='worker_side/add_movie.html', context=context)

def add_sound_recording(request):
    context = {'form': AddSoundRecordingForm()}

    if request.method == 'POST':
        print("CO PRZYSZŁO", request.POST)
        form = AddSoundRecordingForm(request.POST, request.FILES)
        if form.is_valid():
            data_to_summary = form.save()
            return render(request, template_name='worker_side/item_summary.html', context=data_to_summary)
        else:
            print("BŁĘDY: ", form.errors, "\nDATA: ", form.cleaned_data)
            messages.error(request, f'Form filled with invalid informations!')
            return redirect('worker_side-add_sound_recording')
    else:
        form = AddSoundRecordingForm(request.POST, request.FILES)
        return render(request, template_name='worker_side/add_sound_recording.html', context=context)

