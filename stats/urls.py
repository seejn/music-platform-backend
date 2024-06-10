from django.urls import path
from .views import user_stats_view, artist_stats_view, favorite_album_stats_view, favorite_playlist_stats_view, track_report_stats_view

urlpatterns = [
    path('users/', user_stats_view, name='user-stats'),
    path('artists/', artist_stats_view, name='artist-stats'),
    path('favorite-albums/', favorite_album_stats_view, name='favorite-album-stats'),
    path('favorite-playlists/', favorite_playlist_stats_view, name='favorite-playlist-stats'),
    path('track-reports/', track_report_stats_view, name='track-report-stats'),
]
