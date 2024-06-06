from django.urls import path
from . import views

urlpatterns = [
    path('get_all_genres/', views.get_all_genres, name="get_all_genres")
]