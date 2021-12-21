from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="worker_side-home"),
    path('register-user/', views.register_user, name="worker_side-register_user"),
    path('add-book/', views.add_book, name="worker_side-add_book"),
    path('add-movie/', views.add_movie, name="worker_side-add_movie"),
]