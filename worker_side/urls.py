from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="worker_side-home"),
    path('register-user/', views.register_user, name="worker_side-register_user"),
    path('log-in/', views.log_in, name="worker_side-log_in"),
]
