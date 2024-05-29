from django.urls import path
from .views import get_all_artist,get_current_artist

urlpatterns = [
    path('artists/', get_all_artist, name='get_all_artist'),
    path('artists/<int:pk>/', get_current_artist, name='current_artist_detail'),
]
