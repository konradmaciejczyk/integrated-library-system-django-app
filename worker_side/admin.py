from django.contrib import admin
from worker_side.models import Book, Condition, Publisher, Availability, Author

admin.site.register(Book)
admin.site.register(Availability)
admin.site.register(Condition)
admin.site.register(Publisher)
admin.site.register(Author)
