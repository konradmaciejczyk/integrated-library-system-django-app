from django.urls import path
from . import views
import user_side

urlpatterns = [
    path('', views.home, name="user_side-home"),
    path('search', views.search, name="user_side-search"),
    path('log-in', views.log_in, name="user_side-log_in")
]
