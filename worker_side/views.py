from django.db.models import Value
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http.response import JsonResponse
from flask import request_finished 
from user_side.models import BookOrder, MovieOrder, SoundRecordingOrder, Status
from .forms import  AddBookForm, ClientRegistrationForm, AddMovieForm, AddSoundRecordingForm
from datetime import datetime, timedelta
from accounts.models import Citizenship
from worker_side.models import Author, Director, Publisher, Screenwriter, Book, Movie, SoundRecording
from django.core.mail import send_mail
from accounts.decorators import is_staff_user
import json

@is_staff_user
def home(request):
    status = Status.objects.get(id=1)
    number_of_orders = len(BookOrder.objects.all().filter(status=status)) + len(SoundRecordingOrder.objects.all().filter(status=status)) + len(MovieOrder.objects.all().filter(status=status))
    print(number_of_orders)

    if 'order_status' in request.GET:
        return JsonResponse(number_of_orders, safe=False)
    else:
        return render(request, 'worker_side/home.html', context={'number_of_orders':number_of_orders})

@is_staff_user 
def register_user(request):
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

@is_staff_user
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

@is_staff_user
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

@is_staff_user
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

@is_staff_user
def placed_orders(request):
    status = Status.objects.get(id=1)
    if request.method == "GET":
        items = list(BookOrder.objects.all().annotate(item_type=Value('Book')).filter(status=status)) + list(MovieOrder.objects.all().annotate(item_type=Value("Movie/Film")).filter(status=status)) + list(SoundRecordingOrder.objects.all().annotate(item_type=Value("Sound recording")).filter(status=status))

        context = {
        'items': items, 'title': 'Placed orders'
        }

        return render(request, template_name='worker_side/orders.html', context=context)
    else:
        try: 
            item, itemID = json.loads(request.body)['itemID'].split("-")
            status = Status.objects.get(id=2)
            item_type, item_title, client_name, client_email = None, None, None, None
            if item == "Book":
                book = BookOrder.objects.get(id=itemID)            
                book.status = status
                item_type = "book"
                item_title = book.item.title
                client_name = book.client.user.first_name
                client_email = book.client.user.email
                book.save()
            elif item == "Movie/Film":
                movie = MovieOrder.objects.get(id=itemID)
                movie.status = status
                item_type = "movie"
                item_title = movie.item.title
                client_name = movie.client.user.first_name
                client_email = movie.client.user.email
                movie.save()
            elif item == "Sound recording":
                sr = SoundRecordingOrder.objects.get(id=itemID)
                sr.status = status
                item_type = "sound recording"
                item_title = sr.item.title
                client_name = sr.client.user.first_name
                client_email = sr.client.user.email
                sr.save()

            subject = 'Online Library Catalog - Your item is waiting for pickup!'
            message = """ 
            Hello {},

            The following {}:
            {}  is waiting for you at library for pickup.



            This message was created created automatically. Please do not respond.

            Sincerly,
            Online Library Catalog team
            """.format(client_name, item_type, item_title)
            #send_mail(subject, message, 'conrad2048@gmail.com', (client_email,))
            return JsonResponse(["OK!", item+'-'+itemID], safe=False)
        except:
            return  JsonResponse("ERROR!", safe=False)
        
@is_staff_user
def waiting_orders(request):
    status = Status.objects.get(id=2)
    if request.method == "GET":
        items = list(BookOrder.objects.all().annotate(item_type=Value('Book')).filter(status=status)) + list(MovieOrder.objects.all().annotate(item_type=Value("Movie/Film")).filter(status=status)) + list(SoundRecordingOrder.objects.all().annotate(item_type=Value("Sound recording")).filter(status=status))

        context = {
            'title': 'Ready for pickup', 'items': items
        }

        return render(request, template_name='worker_side/orders.html', context=context)
    else:
        try: 
            item, itemID = json.loads(request.body)['itemID'].split("-")
            status = Status.objects.get(id=3)
            if item == "Book":
                book_order = BookOrder.objects.get(id=itemID)  
                book = book_order.item
                book.due_date = datetime.today() + timedelta(31)    
                book_order.timestamp = datetime.today() + timedelta(31)
                book_order.status = status
                book_order.save()
                book.save()
            elif item == "Movie/Film":
                movie_order = MovieOrder.objects.get(id=itemID)
                movie = movie_order.item
                movie.due_date = datetime.today() + timedelta(31) 
                movie_order.timestamp = datetime.today() + timedelta(31)
                movie_order.status = status
                movie.save()
                movie_order.save()
            elif item == "Sound recording":
                sr_order = SoundRecordingOrder.objects.get(id=itemID)
                sr = sr_order.item
                sr_order.timestamp = datetime.today() + timedelta(31)
                sr.due_date = datetime.today() + timedelta(31) 
                sr_order.status = status
                sr.save()
                sr_order.save()
            
            return JsonResponse(["OK!", item+'-'+itemID], safe=False)
        except:
            return JsonResponse("ERROR!", safe=False)

@is_staff_user
def borrowed_items(request):
    status = Status.objects.get(id=3)
    if request.method == "GET":
        items = list(BookOrder.objects.all().annotate(item_type=Value('Book')).filter(status=status)) + list(MovieOrder.objects.all().annotate(item_type=Value("Movie/Film")).filter(status=status)) + list(SoundRecordingOrder.objects.all().annotate(item_type=Value("Sound recording")).filter(status=status))

        context = {
            'title': 'Borrowed items', 'items': items
        }

        return render(request, template_name="worker_side/orders.html", context=context)
    else:
        item, itemID = json.loads(request.body)['itemID'].split("-")

        if item == "Book":
            book_order = BookOrder.objects.get(id=itemID)
            client = book_order.client    
            book = book_order.item
            book.due_date = None
            book.availability = book_order.default_availability
            book.save()
            client.current_borrows -= 1 
            book_order.delete()
            client.save()
        elif item == "Movie/Film":
            movie_order = MovieOrder.objects.get(id=itemID)
            client = movie_order.client
            movie = movie_order.item
            movie.due_date = None
            movie.availability = movie_order.default_availability
            movie.save()
            client.current_borrows -= 1
            movie_order.delete()
            client.save()
        elif item == "Sound recording":
            sr_order = SoundRecordingOrder.objects.get(id=itemID)
            client = sr_order.client
            sr = sr_order.item
            sr.due_date = None
            sr.availability = sr_order.default_availability
            sr.save()
            client.current_borrows -= 1
            sr_order.delete()
            client.save()
        
        return JsonResponse(["OK!", item+'-'+itemID], safe=False)

@is_staff_user
def modify_item(request):
    if request.method == "GET":
        context = {'directors': Director.objects.all(),
               'screenwriters': Screenwriter.objects.all(),
               'authors': Author.objects.all(),
               'publishers': Publisher.objects.all()}

        return render(request, template_name="worker_side/modify_item.html", context=context)
    else:
        data = json.loads(request.body)
        phrase = data['phrase']
        item_type = data['item_type']
        phrase_type = data['phrase_type']

        result = None
        if item_type == "Author":
            item = Author.objects.get(id=phrase) if phrase_type == "ID" else Author.objects.get(name__icontains=phrase)
            result = {'name': item.name}
        elif item_type == "Publisher":
            item = Publisher.objects.get(id=phrase) if phrase_type == 'ID' else Publisher.objects.get(name__icontains=phrase)
            result = {'name': item.name}
        elif item_type == "Director":
            item = Director.objects.get(id=phrase) if phrase_type == 'ID' else Director.objects.get(name__icontains=phrase)
            result = {'name': item.name}
        elif item_type == "Screenwriter":
            item = Screenwriter.objects.get(id=phrase) if phrase_type == 'ID' else Screenwriter.objects.get(name__icontains=phrase)
            result = {'name': item.name}
        elif item_type == "Book":
            item = Book.objects.get(id=phrase) if phrase_type == "ID" else Book.objects.get(title__icontains=phrase)
            authors = ",".join([author.name for author in item.author.all()])

            result = {'isbn': item.isbn, 'title': item.title, 'full_title': item.full_title, 'author': authors, 'pub_year': item.pub_year, 'publisher': item.publisher.name, 'description': item.description, 'availability': 1 if item.availability.name == "Available to borrow" else 2, 'condition': 1 if item.condition.name == "Good" else 2}
        print(result)
        #item.availability.name

        return JsonResponse(["OK!", item_type, result], safe=False)



