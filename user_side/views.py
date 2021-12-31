from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from user_side.forms import SearchForm
from worker_side.models import Author, Book, Director, Movie, SoundRecording

def get_books(title, author, output):
    results =  Book.objects.raw("SELECT * FROM worker_side_book AS book INNER JOIN (SELECT * FROM worker_side_author AS author INNER JOIN worker_side_book_author AS book_author ON author.id=book_author.author_id) AS total ON total.book_id=book.id WHERE LOWER(book.title) LIKE LOWER(%s) AND LOWER(total.name) LIKE LOWER(%s)", ["%"+title+"%", author+"%"]) if author else  Book.objects.raw("SELECT * FROM worker_side_book AS book INNER JOIN (SELECT * FROM worker_side_author AS author INNER JOIN worker_side_book_author AS book_author ON author.id=book_author.author_id) AS total ON total.book_id=book.id WHERE LOWER(book.title) LIKE LOWER(%s)", ["%"+title+"%"])

    book = {}

    for result in results:
        book['type'] = 1
        book['title'] = result.title
        book['full_title'] = result.full_title
        author = ", ".join([author.name for author in result.author.all()])
        book['author'] = author if author else "author(s) unknown"
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

def get_movies(title, director_screenwriter, output):
    results = Movie.objects.raw("SELECT * FROM worker_side_movie AS movie INNER JOIN worker_side_movie_director AS movie_director ON movie.id=movie_director.movie_id INNER JOIN worker_side_director AS director ON director.id=movie_director.director_id WHERE LOWER(title) LIKE LOWER(%s) AND LOWER(director.name) LIKE LOWER (%s)", ["%"+title+"%", director_screenwriter+"%"]) if director_screenwriter else Movie.objects.raw("SELECT * FROM worker_side_movie AS movie INNER JOIN worker_side_movie_director AS movie_director ON movie.id=movie_director.movie_id INNER JOIN worker_side_director AS director ON director.id=movie_director.director_id WHERE LOWER(title) LIKE LOWER(%s)", ["%"+title+"%"])

    if len(results) < 1:
        print(len(results))
        results = Movie.objects.raw("SELECT * FROM worker_side_movie AS movie INNER JOIN worker_side_movie_screenwriter AS movie_screenwriter ON movie.id=movie_screenwriter.movie_id INNER JOIN worker_side_screenwriter AS screenwriter ON screenwriter.id=movie_screenwriter.screenwriter_id WHERE LOWER(title) LIKE LOWER(%s) AND LOWER(screenwriter.name) LIKE LOWER(%s)", ["%"+title+"%", director_screenwriter+"%"])
        
        
    movie = {}

    for result in results:
        movie['type'] = 2
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

def get_sound_recordings(title, author, output):
    
    results = SoundRecording.objects.raw("SELECT * FROM worker_side_soundrecording AS soundrecording INNER JOIN worker_side_soundrecording_author AS soundrecording_author ON soundrecording.id=soundrecording_author.soundrecording_id INNER JOIN worker_side_author AS author ON author.id=soundrecording_author.author_id WHERE LOWER(title) LIKE LOWER(%s) AND LOWER(author.name) LIKE LOWER(%s);", ["%"+title+"%", author+"%"]) if author else  SoundRecording.objects.raw("SELECT * FROM worker_side_soundrecording AS soundrecording INNER JOIN worker_side_soundrecording_author AS soundrecording_author ON soundrecording.id=soundrecording_author.soundrecording_id INNER JOIN worker_side_author AS author ON author.id=soundrecording_author.author_id WHERE LOWER(title) LIKE LOWER(%s);", ["%"+title+"%"])


    soundrecording = {}

    for result in results:
        soundrecording['type'] = 3
        soundrecording['title'] = result.title
        soundrecording['full_title'] = result.full_title
        author = ", ".join([author.name for author in result.author.all()])
        soundrecording['author'] = author if author else "author unknown"
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
    if 'title' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data
            sets = []
            output = []

            if data['book']:
                get_books(data['title'], data['author'], output)
                sets.append("books")

            if data['movie']:
                get_movies(data['title'], data['author'], output)
                sets.append('movies')

            if data['sr']:
               get_sound_recordings(data['title'], data['author'], output)
               sets.append('sound recordings')

            if len(sets) > 1:
                sets.insert(len(sets) - 1, "and")

            result = ", ".join(sets[0:-2]) +" "
            result += " ".join(sets[-2:])
            
            context = {
                'number_of_results': len(output),
                'fields':{'title': data['title'], 'author': data['author'], 'filters': result},
                'results': output
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
    return render(request, "user_side/profile.html")

def home(request):
    return render(request, "user_side/home.html")