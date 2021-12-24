from django.contrib import admin
from worker_side.models import Book, Condition, Director, Movie, Publisher, Availability, Author, Screenwriter, SoundRecording

admin.site.register(Book)
admin.site.register(Movie)
admin.site.register(SoundRecording)
admin.site.register(Availability)
admin.site.register(Condition)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Director)
admin.site.register(Screenwriter)
