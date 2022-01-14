from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="worker_side-home"),
    path('register-user/', views.register_user, name="worker_side-register_user"),
    path('add-book/', views.add_book, name="worker_side-add_book"),
    path('add-movie/', views.add_movie, name="worker_side-add_movie"),
    path('add-sound-recording/', views.add_sound_recording, name="worker_side-add_sound_recording"),
    path('placed-orders', views.placed_orders, name="worker_side-placed_orders"),
    path('waiting-orders', views.waiting_orders, name="worker_side-waiting_orders"),
    path('borrowed-items', views.borrowed_items, name="worker_side-borrowed_items")
]