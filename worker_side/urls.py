from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="worker_side-home"),
    path('register-user/', views.register_user, name="worker_side-register_user"),
    path('add-item/', views.add_item, name="worker_side-add_item")
]