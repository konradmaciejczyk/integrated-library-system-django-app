from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="user_side-home"),
    path('search', views.search, name="user_side-search"),
]
