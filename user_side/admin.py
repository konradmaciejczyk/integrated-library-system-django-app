from django.contrib import admin
from .models import Citizenship, Client, IDType, Gender, Occupation, User

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Citizenship)
admin.site.register(Gender)
admin.site.register(IDType)
admin.site.register(Occupation)
