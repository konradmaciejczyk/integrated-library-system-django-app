# Konrad Maciejczyk, 2021-2022
from os import CLD_EXITED, sched_setscheduler, stat
from django.http.response import JsonResponse
import json
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from user_side.forms import SearchForm
from user_side.models import Client
from worker_side.models import Book, Movie, SoundRecording
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import User
from django.contrib import messages
from user_side.models import BookOrder, SoundRecordingOrder, MovieOrder, Status 

def get_books(title, author, output, authors):
    results =  Book.objects.raw("SELECT * FROM worker_side_book book JOIN (SELECT * FROM worker_side_author author JOIN worker_side_book_author book_author ON author.id=book_author.author_id) total ON total.book_id=book.id WHERE LOWER(book.title) LIKE LOWER(%s) AND LOWER(total.name) LIKE LOWER(%s);", ["%"+title+"%", author+"%"]) if author else  Book.objects.raw("SELECT * FROM worker_side_book book JOIN (SELECT * FROM worker_side_author author JOIN worker_side_book_author book_author ON author.id=book_author.author_id) total ON total.book_id=book.id WHERE LOWER(book.title) LIKE LOWER(%s)", ["%"+title+"%"])

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
        
        output.append(book)
        book = {}

def get_movies(title, director_screenwriter, output, authors):
    results = Movie.objects.raw("SELECT * FROM worker_side_movie movie JOIN worker_side_movie_director movie_director ON movie.id=movie_director.movie_id JOIN worker_side_director director ON director.id=movie_director.director_id WHERE LOWER(title) LIKE LOWER(%s) AND LOWER(director.name) LIKE LOWER (%s);", ["%"+title+"%", director_screenwriter+"%"]) if director_screenwriter else Movie.objects.raw("SELECT * FROM worker_side_movie movie JOIN worker_side_movie_director movie_director ON movie.id=movie_director.movie_id JOIN worker_side_director director ON director.id=movie_director.director_id WHERE LOWER(title) LIKE LOWER(%s);", ["%"+title+"%"])

    if len(results) < 1:
        results = Movie.objects.raw("SELECT * FROM worker_side_movie AS movie INNER JOIN worker_side_movie_screenwriter AS movie_screenwriter ON movie.id=movie_screenwriter.movie_id INNER JOIN worker_side_screenwriter AS screenwriter ON screenwriter.id=movie_screenwriter.screenwriter_id WHERE LOWER(title) LIKE LOWER(%s) AND LOWER(screenwriter.name) LIKE LOWER(%s)", ["%"+title+"%", director_screenwriter+"%"])
        
        
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

        output.append(movie)
        movie = {}

def get_sound_recordings(title, author, output, authors):    
    results = SoundRecording.objects.raw("SELECT * FROM worker_side_soundrecording AS soundrecording INNER JOIN worker_side_soundrecording_author AS soundrecording_author ON soundrecording.id=soundrecording_author.soundrecording_id INNER JOIN worker_side_author AS author ON author.id=soundrecording_author.author_id WHERE LOWER(title) LIKE LOWER(%s) AND LOWER(author.name) LIKE LOWER(%s);", ["%"+title+"%", author+"%"]) if author else  SoundRecording.objects.raw("SELECT * FROM worker_side_soundrecording AS soundrecording INNER JOIN worker_side_soundrecording_author AS soundrecording_author ON soundrecording.id=soundrecording_author.soundrecording_id INNER JOIN worker_side_author AS author ON author.id=soundrecording_author.author_id WHERE LOWER(title) LIKE LOWER(%s);", ["%"+title+"%"])

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

        output.append(soundrecording)
        soundrecording = {}

def search(request):
    if 'title' or 'author' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data

            
            # if data['title'] == '' and data['author'] == '':
            #     context = {'number_of_results': 0, 'fields':{'title': data['title'], 'author': data['author'], 'filters': "books"}}
            #     return render(request, "user_side/search.html", context)

            sets = []
            output = []
            authors = set()

            if data['book']:
                get_books(data['title'], data['author'], output, authors)
                sets.append("books")
            if data['movie']:
                get_movies(data['title'], data['author'], output, authors)
                sets.append('movies')

            if data['sr']:
               get_sound_recordings(data['title'], data['author'], output, authors)
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
                'cart_items': request.session['cart'] if 'cart' in request.session else 'Ni ma'
            }

            return render(request, "user_side/search.html", context)
        else:
            return redirect('user_side-home')
    else:
        return redirect("user_side-home")

def log_in(request):
    return render(request, "user_side/log_in.html")

@login_required
def profile(request):
    context = {
        'cart_status': len(request.session['cart']) if 'cart' in request.session else 0
    }
    return render(request, "user_side/profile.html", context=context)

def home(request):
    context = {
        'cart_status': len(request.session['cart']) if 'cart' in request.session else 0
    }

    return render(request, "user_side/home.html", context)

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

        print("KOSZYK: ", request.session['cart'])

        request.session.modified = True

        return JsonResponse(request.session['cart'], safe=False)
    else:
        return redirect('user_side-home')

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
            for order in request.session['cart']:
                item_type, item_id = order.split('-')                
                if item_type == '1':
                    item = Book.objects.get(id=item_id)                    
                    order = BookOrder.objects.create(client=logged_client, item=item, status = status)
                elif item_type == '2':
                    item = Movie.objects.get(id=item_id)
                    order = MovieOrder.objects.create(client=logged_client, item=item, status=status)
                elif item_type == '3':
                    item = SoundRecording.objects.get(id=item_id)
                    order = SoundRecordingOrder.objects.create(item=item, client=logged_client, status=status)

            logged_client.current_borrows += len(request.session['cart'])
            logged_client.save()
            request.session['cart'] = []
            request.session.modified = True
            
            messages.success(request, 'Your order has been placed. You\'ll receive e-mail, when your items are ready to be picked up.')
            return redirect('user_side-home')
    
    return render(request, template_name='user_side/cart.html', context=context)