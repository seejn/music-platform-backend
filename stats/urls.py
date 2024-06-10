from django.urls import path
from . import views

urlpatterns = [
    path('artists/songs/playlist-counts/', views.all_artists_song_playlist_counts, name='all-artists-song-playlist-counts'),
    path('artists/albums/favorites/', views.all_artists_album_favorites, name='all-artists-album-favorites'),
    path('artists/albums/counts/', views.artist_album_counts, name='artist-album-counts'),
    path('artists/total/', views.total_artists, name='total-artists'),
    path('users/total/', views.total_users, name='total-users'),
]
