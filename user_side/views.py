# Konrad Maciejczyk, 2021-2022
from os import sched_setscheduler
from django.http.response import JsonResponse
import json
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from user_side.forms import SearchForm
from user_side.models import Client
from worker_side.models import Book, Movie, SoundRecording
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import User

def get_books(title, author, output, authors):
    results =  Book.objects.raw("SELECT * FROM worker_side_book AS book INNER JOIN (SELECT * FROM worker_side_author AS author INNER JOIN worker_side_book_author AS book_author ON author.id=book_author.author_id) AS total ON total.book_id=book.id WHERE LOWER(book.title) LIKE LOWER(%s) AND LOWER(total.name) LIKE LOWER(%s)", ["%"+title+"%", author+"%"]) if author else  Book.objects.raw("SELECT * FROM worker_side_book AS book INNER JOIN (SELECT * FROM worker_side_author AS author INNER JOIN worker_side_book_author AS book_author ON author.id=book_author.author_id) AS total ON total.book_id=book.id WHERE LOWER(book.title) LIKE LOWER(%s)", ["%"+title+"%"])

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
    results = Movie.objects.raw("SELECT * FROM worker_side_movie AS movie INNER JOIN worker_side_movie_director AS movie_director ON movie.id=movie_director.movie_id INNER JOIN worker_side_director AS director ON director.id=movie_director.director_id WHERE LOWER(title) LIKE LOWER(%s) AND LOWER(director.name) LIKE LOWER (%s)", ["%"+title+"%", director_screenwriter+"%"]) if director_screenwriter else Movie.objects.raw("SELECT * FROM worker_side_movie AS movie INNER JOIN worker_side_movie_director AS movie_director ON movie.id=movie_director.movie_id INNER JOIN worker_side_director AS director ON director.id=movie_director.director_id WHERE LOWER(title) LIKE LOWER(%s)", ["%"+title+"%"])

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

            print(data)
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
           
            print(authors)
            
            context = {
                'number_of_results': len(output),
                'fields':{'title': data['title'], 'author': data['author'], 'filters': result},
                'results': results,
                'authors': list(authors),
                'pages': pages,
                'last_page': paginator.num_pages,
                'start_loop': divide_by * (results.number - 1),
                'cart_status': len(request.session['cart']) if 'cart' in request.session else 0
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
    data = json.loads(request.body)
    action = data['action']
    print(data)

    if 'cart' not in request.session:
        request.session['cart'] = []
    
    if action == 1:
        print("!!!")
        request.session['cart'].append(data['productID'])
    elif action == 2:
        request.session['cart'].remove(data['productID'])

    
    request.session.modified = True

    print("SESSION STORE: ", request.session['cart'], len(request.session['cart']))
    return JsonResponse(len(request.session['cart']), safe=False)

def cart(request):
    results = []
    items = []

    for item in request.session['cart']:
        item_type, item_id = item.split('-')
        print(item_type, item_id)

        if item_type == '1':
            print("TU KURWA")
            aux = Book.objects.get(id=item_id)

            book = {}
            book['type'] = 1
            book['title'] = aux.title
            book['full_title'] = aux.full_title
            author = [author.name for author in aux.author.all()]
            if author:
                author = ', '.join(author)
            else:
                author = "author(s) unknown"
            book['author'] = author
            book['isbn'] = aux.isbn if aux.isbn else 'isbn not available'
            book['id'] = aux.id
            book['publisher'] = aux.publisher.name if aux.publisher else "publisher unknown"
            book['pub_year'] = aux.pub_year if aux.pub_year else "publication year unknown"
            book['description'] = aux.description
            book['condition'] = aux.condition.name
            book['availability'] = aux.availability.name
            book['cover'] = aux.cover.url

            results.append(book)

        elif item_type == '2':
            items.append(Movie.objects.get(id=item_id))
        elif item_type == '3':
            items.append(SoundRecording.objects.get(id=item_id))

    logged_user = User.objects.get(email=request.user.email)
    logged_client = Client.objects.get(user = logged_user)
        
    context = {
        'results': results,
        'client_borrows': logged_client.borrows_max - logged_client.current_borrows
    }

    
    return render(request, template_name='user_side/cart.html', context=context)