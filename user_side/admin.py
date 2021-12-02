from django.contrib import admin
from .models import Citizenship, Client, Gender, IDDocumentType, Occupation

admin.site.register(Client)
admin.site.register(Citizenship)
admin.site.register(Occupation)
admin.site.register(Gender)
admin.site.register(IDDocumentType)

