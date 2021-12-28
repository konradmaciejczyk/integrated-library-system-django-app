from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from user_side.forms import SearchForm
from worker_side.models import Author, Book, Director, Movie

def get_books(title, author):
    try:     
        results = None   
        if author:
            results = Author.objects.get(name__istartswith=author).book_set.all().filter(title__istartswith=title)
        else:
            results = Book.objects.filter(title__icontains=title)
        book = {}
        output = []
        print("KSIAZKI:", results)

        for result in results:
            book['title'] = result.title
            book['full_title'] = result.full_title
            author = ", ".join([author.name for author in result.author.all()])
            book['author'] = author if author else "author(s) unknown"
            book['isbn'] = result.isbn if result.isbn else 'isbn not available'
            book['id'] = result.id
            book['publisher'] = result.publisher.name if result.publisher.name else "publisher unknown"
            book['pub_year'] = result.pub_year if result.pub_year else "publication year unknown"
            book['description'] = result.description
            book['condition'] = result.condition.name
            book['availability'] = result.availability.name
            book['cover'] = result.cover.url

            output.append(book)
            book = {}
    except:
        output = {}

    return output

def get_movies(title, director):
    try:
        results = None
        if director:
                results = Director.objects.get(name__istartswith=director).movie_set.all().filter(title__istartswith=title)
        else:
            results = Movie.objects.filter(title__icontains=title)
    


        results = Movie.objects.filter(title__istartswith=title)
        movie = {}
        output = []
        print("FILMY:", results)

        for result in results:
            movie['title'] = result.title
            movie['full_title'] = result.full_title
            director = ", ".join([director.name for director in result.director.all()])
            movie['director'] = director if director else "director unknown"
            screenwriter = ", ".join([screenwriter.name for screenwriter in result.screenwriter.all()])
            movie['screenwriter'] = screenwriter if screenwriter else "screenwriter(s) unknown"
            movie['id'] = result.id
            movie['pub_year'] = result.pub_year if result.pub_year else "publication year unknown"
            movie['description'] = result.description
            movie['condition'] = result.condition.name
            movie['availability'] = result.availability.name
            movie['cover'] = result.cover.url

            output.append(movie)
            movie = {}
     
    except:
        output = {}
  
    return output

def home(request):
    return render(request, "user_side/home.html")

def search(request):
    if 'title' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            number_of_results = 0
            data = form.cleaned_data
            print("CO PRZYSZŁO: ", data)
            books = {}
            movies = {}
            sr = {}

            if data['book']:
                books = get_books(data['title'], data['author'])

            if data['movie']:
                movies = get_movies(data['title'], data['author'])

           
            number_of_results = len(books) + len(movies)
            
            context = {
                'number_of_results': number_of_results,
                'fields':{'title': data['title'], 'author': data['author'], 'filters': "books, movies and sound recordings" },
                'books': books,
                'movies': movies
            }

        #print("DANE:", context)
            return render(request, "user_side/search.html", context)
        else:
            return redirect('user_side-home')
    else:
        return redirect("user_side-home")

def log_in(request):
    return render(request, "user_side/log_in.html")

@login_required
def profile(request):
    return render(request, "user_side/profile.html")