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
    path('borrowed-items', views.borrowed_items, name="worker_side-borrowed_items"),
    path('modify-item/', views.modify_item, name="worker_side-modify_item"),
    path('modify-item/edit-author/', views.edit_author, name="worker_side-edit_author"),
    path('modify-item/edit-director/', views.edit_director, name="worker_side-edit_director"),
    path('modify-item/edit-screenwriter/', views.edit_screenwriter, name="worker_side-edit_screenwriter"),
    path('modify-item/edit-publisher/', views.edit_publisher, name="worker_side-edit_publisher"),
    path('modify-item/edit-book/', views.edit_book, name="worker_side-edit_book"),
    path('modify-item/edit-movie/', views.edit_movie, name="worker_side-edit_movie"),
    path('modify-client', views.modify_client, name="worker_side-modify_client")
]