from django.shortcuts import render, redirect
from django.contrib import messages

from user_side.models import BookOrder
from .forms import  AddBookForm, ClientRegistrationForm, AddMovieForm, AddSoundRecordingForm
from datetime import datetime, timedelta
from accounts.models import Citizenship
from worker_side.models import Author, Director, Publisher, Screenwriter
from django.core.mail import send_mail

def home(request):
    number_of_orders = BookOrder.objects.raw("(SELECT 'Book' as item_type, *  FROM user_side_bookorder WHERE status_id = 1 UNION SELECT 'Movie/Film' as item_type, * FROM user_side_movieorder WHERE status_id = 1 UNION SELECT 'Sound Recording' as item_type, * FROM user_side_soundrecordingorder WHERE status_id = 1) ORDER BY timestamp;")
    print("TU KURWA: ", number_of_orders[:])

    return render(request, 'worker_side/home.html', context={'number_of_orders': len(number_of_orders[:])})

def register_user(request):
    password = None
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            data_to_summary = form.save()

            subject = 'Online Library Catalog - library registration confimation'
            message = """ 
            Hello {},

            You have registred yourself in our Library.
            You can now use our Online Platform to search and order items from Library.

            Your password: {}


            This message was created created automatically. Please do not respond.

            Sincerly,
            Online Library Catalog team
            """.format(data_to_summary['first_name'], data_to_summary['password'])
            to = form.cleaned_data['email']
            send_mail(subject, message, 'conrad2048@gmail.com', (to,))

            return render(request, template_name="worker_side/register_summary.html", context = data_to_summary)
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
        form = AddBookForm(request.POST, request.FILES)
        if form.is_valid():
            data_to_summary = form.save()
            return render(request, template_name='worker_side/item_summary.html', context=data_to_summary)
        else:
            messages.error(request, f'Form filled with invalid informations!')
            return redirect('worker_side-add_book')
    else:
        form = AddBookForm(request.POST, request.FILES)
        return render(request, template_name='worker_side/add_book.html', context=context)

def add_movie(request):
    context = {'directors': Director.objects.all(),
               'screenwriters': Screenwriter.objects.all(),
               'form': AddMovieForm()}

    if request.method == 'POST':
        form = AddMovieForm(request.POST, request.FILES)
        if form.is_valid():
            data_to_summary = form.save()
            return render(request, template_name='worker_side/item_summary.html', context=data_to_summary)
        else:
            messages.error(request, f'Form filled with invalid informations!')
            return redirect('worker_side-add_movie')
    else:
        form = AddMovieForm(request.POST, request.FILES)
        return render(request, template_name='worker_side/add_movie.html', context=context)

def add_sound_recording(request):
    context = {'form': AddSoundRecordingForm(),
    'authors': Author.objects.all(),
    'publishers': Publisher.objects.all()}

    if request.method == 'POST':
        form = AddSoundRecordingForm(request.POST, request.FILES)
        if form.is_valid():
            data_to_summary = form.save()
            return render(request, template_name='worker_side/item_summary.html', context=data_to_summary)
        else:
            messages.error(request, f'Form filled with invalid informations!')
            return redirect('worker_side-add_sound_recording')
    else:
        form = AddSoundRecordingForm(request.POST, request.FILES)
        return render(request, template_name='worker_side/add_sound_recording.html', context=context)

def placed_orders(request):
    items = BookOrder.objects.raw("(SELECT 'Book' as item_type, *  FROM user_side_bookorder WHERE status_id = 1 UNION SELECT 'Movie/Film' as item_type, * FROM user_side_movieorder WHERE status_id = 1 UNION SELECT 'Sound Recording' as item_type, * FROM user_side_soundrecordingorder WHERE status_id = 1) ORDER BY timestamp;")

    context = {
        'items': items, 'title': 'Placed orders'
    }

    return render(request, template_name='worker_side/orders.html', context=context)

def waiting_orders(request):
    items = BookOrder.objects.raw("(SELECT 'Book' as item_type, *  FROM user_side_bookorder WHERE status_id = 2 UNION SELECT 'Movie/Film' as item_type, * FROM user_side_movieorder WHERE status_id = 2 UNION SELECT 'Sound Recording' as item_type, * FROM user_side_soundrecordingorder WHERE status_id = 2) ORDER BY timestamp;")

    context = {
        'title': 'Waiting orders', 'items': items
    }

    return render(request, template_name='worker_side/orders.html', context=context)

