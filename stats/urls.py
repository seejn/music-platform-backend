from django.urls import path
from . import views

urlpatterns = [
    path('artists/songs/playlist-counts/', views.all_artists_song_playlist_counts, name='all-artists-song-playlist-counts'),
    path('artists/albums/favorites/', views.all_artists_album_favorites, name='all-artists-album-favorites'),
]
