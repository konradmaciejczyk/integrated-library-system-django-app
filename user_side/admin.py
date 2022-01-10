from django.contrib import admin
from .models import BookOrder, Citizenship, Client, IDType, MovieOrder, Occupation, SoundRecordingOrder, Status, User

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Citizenship)
admin.site.register(IDType)
admin.site.register(Occupation)
admin.site.register(BookOrder)
admin.site.register(MovieOrder)
admin.site.register(SoundRecordingOrder)
admin.site.register(Status)
