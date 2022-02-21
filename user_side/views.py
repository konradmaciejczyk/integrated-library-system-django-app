# Konrad Maciejczyk, 2021-2022
from datetime import datetime, timedelta
from django.http.response import JsonResponse
import json
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from user_side.forms import SearchForm, UpdateClientForm, UpdateUserForm
from user_side.models import Client
from worker_side.models import Availability, Book, Movie, SoundRecording, Author, Director, Screenwriter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import User
from django.contrib import messages
from user_side.models import BookOrder, SoundRecordingOrder, MovieOrder, Status 
from django.db.models import Value
from accounts.decorators import is_normal_user

def get_books(title, author, output, authors, availability):
    results =  Book.objects.raw("SELECT * FROM worker_side_book book JOIN (SELECT * FROM worker_side_author author JOIN worker_side_book_author book_author ON author.id=book_author.author_id) total ON total.book_id=book.id WHERE LOWER(book.title) LIKE LOWER(%s) AND LOWER(total.name) LIKE LOWER(%s)"+availability, ["%"+title+"%", author+"%"]) if author else  Book.objects.raw("SELECT * FROM worker_side_book book WHERE LOWER(title) LIKE LOWER(%s)"+availability, ["%"+title+"%"])

    book = {}

    for result in results:
        book['type'] = 1
        book['title'] = result.title
        book['full_title'] = result.full_title
        author = [author.name for author in result.author.all()]
        if author:
            [authors.add(x) for x in author]
            author = ', '.join(author)
        else:
            author = "author(s) unknown"
        book['author'] = author
        book['isbn'] = result.isbn if result.isbn else 'isbn not available'
        book['id'] = result.id
        book['publisher'] = result.publisher.name if result.publisher else "publisher unknown"
        book['pub_year'] = result.pub_year if result.pub_year else "publication year unknown"
        book['description'] = result.description
        book['condition'] = result.condition.name
        book['availability'] = result.availability.name
        book['cover'] = result.cover.url
        book['due_date'] = result.due_date if result.due_date else False
        
        output.append(book)
        book = {}

def get_movies(title, director_screenwriter, output, authors, availability):
    results = Movie.objects.raw("SELECT * FROM worker_side_movie movie JOIN worker_side_movie_director movie_director ON movie.id=movie_director.movie_id JOIN worker_side_director director ON director.id=movie_director.director_id WHERE LOWER(title) LIKE LOWER(%s) AND LOWER(director.name) LIKE LOWER (%s)"+availability, ["%"+title+"%", director_screenwriter+"%"]) if director_screenwriter else Movie.objects.raw("SELECT * FROM worker_side_movie movie JOIN worker_side_movie_director movie_director ON movie.id=movie_director.movie_id JOIN worker_side_director director ON director.id=movie_director.director_id WHERE LOWER(title) LIKE LOWER(%s)"+availability, ["%"+title+"%"])

    if len(results) < 1:
        results = Movie.objects.raw("SELECT * FROM worker_side_movie AS movie INNER JOIN worker_side_movie_screenwriter AS movie_screenwriter ON movie.id=movie_screenwriter.movie_id INNER JOIN worker_side_screenwriter AS screenwriter ON screenwriter.id=movie_screenwriter.screenwriter_id WHERE LOWER(title) LIKE LOWER(%s) AND LOWER(screenwriter.name) LIKE LOWER(%s)"+availability, ["%"+title+"%", director_screenwriter+"%"]) if director_screenwriter else Movie.objects.raw("SELECT * FROM worker_side_movie movie WHERE LOWER(title) LIKE LOWER(%s)"+availability, ["%"+title+"%"])
        
    movie = {}

    for result in results:
        movie['type'] = 2
        movie['title'] = result.title
        movie['full_title'] = result.full_title
        director = [director.name for director in result.director.all()]
        if director:
            [authors.add(x) for x in director]
            director = ', '.join(director)
        else:
            director = "director(s) unknown"
        movie['director'] = director
        screenwriter = [screenwriter.name for screenwriter in result.screenwriter.all()]
        if screenwriter:
            [authors.add(x) for x in screenwriter]
            screenwriter = ', '.join(screenwriter)
        else:
            screenwriter = 'screenwriter(s) unknown'
        movie['screenwriter'] = screenwriter
        movie['id'] = result.id
        movie['pub_year'] = result.pub_year if result.pub_year else "publication year unknown"
        movie['description'] = result.description
        movie['condition'] = result.condition.name
        movie['availability'] = result.availability.name
        movie['cover'] = result.cover.url
        movie['due_date'] = result.due_date if result.due_date else False        

        output.append(movie)
        movie = {}

def get_sound_recordings(title, author, output, authors, availability):    
    results = SoundRecording.objects.raw("SELECT * FROM worker_side_soundrecording AS soundrecording INNER JOIN worker_side_soundrecording_author AS soundrecording_author ON soundrecording.id=soundrecording_author.soundrecording_id INNER JOIN worker_side_author AS author ON author.id=soundrecording_author.author_id WHERE LOWER(title) LIKE LOWER(%s) AND LOWER(author.name) LIKE LOWER(%s)"+availability, ["%"+title+"%", author+"%"]) if author else SoundRecording.objects.raw("SELECT * FROM worker_side_soundrecording soundrecording WHERE LOWER(title) LIKE LOWER(%s)"+availability, ["%"+title+"%"])

    soundrecording = {}

    for result in results:
        soundrecording['type'] = 3
        soundrecording['title'] = result.title
        soundrecording['full_title'] = result.full_title
        author = [author.name for author in result.author.all()]
        if author:
            [authors.add(x) for x in author]
            author = ', '.join(author)
        else:
            author = "author(s) unknown"
        soundrecording['author'] = author
        soundrecording['id'] = result.id
        soundrecording['pub_year'] = result.pub_year if result.pub_year else "publication year unknown"
        soundrecording['publisher'] = result.publisher.name if result.publisher else "publisher unknown"
        soundrecording['cast'] = result.cast if result.cast else "cast unknown"
        soundrecording['description'] = result.description
        soundrecording['condition'] = result.condition.name
        soundrecording['availability'] = result.availability.name
        soundrecording['cover'] = result.cover.url
        soundrecording['due_date'] = result.due_date if result.due_date else False

        output.append(soundrecording)
        soundrecording = {}

def search(request):
    if 'title' or 'author' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data

            
            if data['title'] == '' and data['author'] == '':
                context = {'number_of_results': 0, 'fields':{'title': data['title'], 'author': data['author'], 'filters': "books"}}
                return render(request, "user_side/search.html", context)

            sets = []
            output = []
            authors = set()

            if data['book']:
                get_books(data['title'], data['author'], output, authors, ' ;' if data['not_available'] else " AND book.availability_id != 3;")
                sets.append("books")
            if data['movie']:
                get_movies(data['title'], data['author'], output, authors, ' ;' if data['not_available'] else " AND movie.availability_id != 3;")
                sets.append('movies')

            if data['sr']:
               get_sound_recordings(data['title'], data['author'], output, authors, ' ;' if data['not_available'] else " AND soundrecording.availability_id != 3;")
               sets.append('sound recordings')

            if len(sets) > 1:
                sets.insert(len(sets) - 1, "and")

            result = ", ".join(sets[0:-2]) +" "
            result += " ".join(sets[-2:])
            
            divide_by = int(data['on_site']) if data['on_site'] else 5
            paginator = Paginator(output, divide_by)
            page = request.GET.get('page')
            
            results = None
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)

            pages = [results.number]
            if results.has_previous():
                pages.insert(0, results.previous_page_number())
            if results.has_next():
                pages.append(results.next_page_number())

            context = {
                'number_of_results': len(output),
                'fields':{'title': data['title'], 'author': data['author'], 'filters': result},
                'results': results,
                'authors': list(authors),
                'pages': pages,
                'last_page': paginator.num_pages,
                'start_loop': divide_by * (results.number - 1),
                'cart_status': len(request.session['cart']) if 'cart' in request.session else 0,
                'cart_items': request.session['cart'] if 'cart' in request.session else []
            }

            return render(request, "user_side/search.html", context)
        else:
            return redirect('user_side-home')
    else:
        return redirect("user_side-home")

def log_in(request):
    return render(request, "user_side/log_in.html")

@is_normal_user
def profile(request):
    client = Client.objects.get(user=request.user)
    if request.method == "GET":
        u_form = UpdateUserForm()
        c_form = UpdateClientForm()
        client_items = list(BookOrder.objects.all().annotate(item_type=Value('Book')).filter(client=client)) + list(MovieOrder.objects.all().annotate(item_type=Value('Movie/Film')).filter(client=client)) + list(SoundRecordingOrder.objects.all().annotate(item_type=Value("Sound recording")).filter(client=client))

        for index, client_item in enumerate(client_items):
            prolong = None
            if client_item.item.due_date:
                prolong = True if (client_item.item.due_date - datetime.today().date()).days < 7 and client_item.prolongs < 4 else False
            else:
                prolong = False
            client_items[index] = (client_item, prolong)

        context = {
            'cart_status': len(request.session['cart']) if 'cart' in request.session else 0,
            'client': client,
            'user_data': {
                'email': request.user.email,
                'phone_num': request.user.phone_number,
                'corr_address': client.corr_address
            },
            'client_items': client_items
        }
        return render(request, "user_side/profile.html", context=context)
    else:
        u_form = UpdateUserForm(request.POST, instance=request.user)
        c_form = UpdateClientForm(request.POST, instance=client)

        if u_form.is_valid() and c_form.is_valid():
            u_form.save()
            c_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('user_side-profile') 
        else:
            messages.error(request, "The data you've sent is not correct. Check your inputs and try again.")
            return redirect('user_side-profile')   

@is_normal_user
def prolong(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_type, item_id = data['item'].split('-')

        if item_type == "Book":
            book_order = BookOrder.objects.get(id=item_id)
            book = book_order.item
            book.due_date = book.due_date + timedelta(31)
            book_order.prolongs += 1
            book_order.save()
            book.save()
        elif item_type == "Movie/Film":
            movie_order = MovieOrder.objects.get(id=item_id)
            movie = movie_order.item
            movie.due_date = movie.due_date + timedelta(31)
            movie_order.prolongs += 1
            movie_order.save()
            movie.save()
        elif item_type == "Sound recording":
            sr_order = SoundRecordingOrder.objects.get(id=item_id)
            sr = sr_order.item
            sr.due_date = sr.due_date + timedelta(31)
            sr_order.prolongs += 1
            sr_order.save()
            sr.save()

        return JsonResponse("OK!", safe=False)
    else:
        return redirect('user_side-profile')

def home(request):
    context = {
        'cart_status': len(request.session['cart']) if 'cart' in request.session else 0,
        'titles': list(set([book.title for book in Book.objects.all()] + [movie.title for movie in Movie.objects.all()] + [sr.title for sr in SoundRecording.objects.all()])),
        'authors': list(set([author.name for author in Author.objects.all()] + [director.name for director in Director.objects.all()] + [screenwriter.name for screenwriter in Screenwriter.objects.all()]))
    }

    return render(request, "user_side/home.html", context)

@is_normal_user
def update_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data['action']

        if 'cart' not in request.session:
            request.session['cart'] = []
        
        if action == 1:
            if data['productID'] not in request.session['cart']:
                request.session['cart'].append(data['productID'])  
        elif action == 2:
            if data['productID'] in request.session['cart']:
                request.session['cart'].remove(data['productID'])
        elif action == 3:
            item_type, item_id = data['productID'].split("-")

            if item_type == "1":
                book = Book.objects.get(id=item_id)
                book_order = BookOrder.objects.get(item=book)
                book_order.reserved_by = Client.objects.get(user=request.user)
                book_order.save()
            elif item_type == "2":
                movie = Movie.objects.get(id=item_id)
                movie_order = MovieOrder.objects.get(item=movie)
                movie_order.reserved_by = Client.objects.get(user=request.user)
                movie_order.save()
            elif item_type == "3":
                sound_recording = SoundRecording.objects.get(id=item_id)
                sound_recording_order = SoundRecordingOrder.objects.get(item=sound_recording)
                sound_recording_order.reserved_by = Client.objects.get(user=request.user)
                sound_recording_order.save()

            return JsonResponse("Item reserved: {}".format(data['productID']), safe=False)

        request.session.modified = True

        return JsonResponse(request.session['cart'], safe=False)
    else:
        return redirect('user_side-home')

@is_normal_user
def cart(request):
    logged_user = User.objects.get(email=request.user.email)
    logged_client = Client.objects.get(user = logged_user)
    client_borrows = logged_client.borrows_max - logged_client.current_borrows

    if request.method == "GET":
        results = []

        for item in request.session['cart']:
            item_type, item_id = item.split('-')

            aux = None
            order_item = {
                'author': '', 'type': '', 'isbn': '', 'publisher': '', 'title': '', 'full_title': '', 'id': '', 'pub_year': '', 'description': '', 'condition': '', 'availability': '', 'cover': ''
            }
            if item_type == '1':
                aux = Book.objects.get(id=item_id)

                author = [author.name for author in aux.author.all()]
                if author:
                    author = ', '.join(author)
                else:
                    author = "author(s) unknown"
                order_item['author'] = author
                order_item['isbn'] = aux.isbn if aux.isbn else 'isbn not available'
                order_item['publisher'] = aux.publisher.name if aux.publisher else "publisher unknown"
            elif item_type == '2':
                aux = Movie.objects.get(id=item_id)

                director = [director.name for director in aux.director.all()]
                if director:
                    director = ', '.join(director)
                else:
                    director = "director(s) unknown"
                order_item['director'] = director
                screenwriter = [screenwriter.name for screenwriter in aux.screenwriter.all()]
                if screenwriter:
                    screenwriter = ', '.join(screenwriter)
                else:
                    screenwriter = 'screenwriter(s) unknown'
                order_item['screenwriter'] = screenwriter
            elif item_type == '3':
                aux = SoundRecording.objects.get(id=item_id)
                order_item['cast'] = aux.cast if aux.cast else "cast unknown"
                order_item['publisher'] = aux.publisher.name if aux.publisher else "publisher unknown"

            order_item['type'] = int(item_type)
            order_item['title'] = aux.title
            order_item['full_title'] = aux.full_title
            order_item['id'] = aux.id
            order_item['pub_year'] = aux.pub_year if aux.pub_year else "publication year unknown"
            order_item['description'] = aux.description
            order_item['condition'] = aux.condition.name
            order_item['availability'] = aux.availability.name
            order_item['cover'] = aux.cover.url

            results.append(order_item)

        
            
        context = {
            'results': results,
            'client_borrows': client_borrows,
            'items_amount': request.session['cart'] if 'cart' in request.session else 0
        }
    else:
        if len(request.session['cart']) > client_borrows:
            messages.error('Failed to place an order. Try again later.')
            return redirect('user_side-home')
        else:
            status = Status.objects.get(id=1)
            availability = Availability.objects.get(id=3)
            for order in request.session['cart']:
                item_type, item_id = order.split('-')                
                if item_type == '1':
                    item = Book.objects.get(id=item_id)                                   
                    order = BookOrder.objects.create(client=logged_client, item=item, status = status)
                    order.default_availability = item.availability
                    item.availability = availability
                    item.save()
                    order.save()     
                elif item_type == '2':
                    item = Movie.objects.get(id=item_id)
                    order = MovieOrder.objects.create(client=logged_client, item=item, status=status)
                    order.default_availability = item.availability
                    item.availability = availability
                    item.save()
                    order.save()
                elif item_type == '3':
                    item = SoundRecording.objects.get(id=item_id)
                    order = SoundRecordingOrder.objects.create(item=item, client=logged_client, status=status)
                    order.default_availability = item.availability
                    item.availability = availability
                    item.save()
                    order.save()                    

            logged_client.current_borrows += len(request.session['cart'])
            logged_client.save()
            request.session['cart'] = []
            request.session.modified = True
            
            messages.success(request, 'Your order has been placed. You\'ll receive e-mail, when your items are ready to be picked up.')
            return redirect('user_side-home')
    
    return render(request, template_name='user_side/cart.html', context=context)
