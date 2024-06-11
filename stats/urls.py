from django.urls import path
from . import views

urlpatterns = [
    path('artists/songs/playlist-counts/', views.all_artists_song_playlist_counts, name='all-artists-song-playlist-counts'),
    path('artist/<int:artist_id>/album/', views.get_artist_album_favourite_stats, name='get_artist_album_favourite_stats'),
    path('artists/albums/favorites/', views.all_artists_album_favorites, name='all-artists-album-favorites'),
    path('artists/albums/counts/', views.artist_album_counts, name='artist-album-counts'),
    path('artists/total/', views.total_artists, name='total-artists'),
    path('users/total/', views.total_users, name='total-users'),
    path('tracks/total/', views.total_tracks, name='total-tracks'),
    path('artist/<int:artist_id>/album-count/',views.artist_album, name='total-artist-album'),
    path('artist/<int:artist_id>/track-count/',views.artist_total_tracks, name='total-artist-track')
]
