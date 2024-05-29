from django.urls import path
from .views import get_all_artist

urlpatterns = [
    path('artists/', get_all_artist, name='get_all_artist'),
]
