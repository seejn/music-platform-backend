from django.urls import path
from . import views

urlpatterns = [
    path('report_track/<int:track_id>/', views.report_track, name="report_track"),
    path('get_all_reported_tracks/', views.get_all_reported_tracks, name="get_all_reported_tracks"),
    path('get_reported_tracks_of_artist/<int:artist_id>/', views.get_reported_tracks_of_artist, name="get_reported_tracks_of_artist"),

    
    path('get_all_banned_tracks/', views.get_all_banned_tracks, name="get_all_banned_tracks"),
    path('get_banned_tracks_of_artist/<int:artist_id>/', views.get_banned_tracks_of_artist, name="get_banned_tracks_of_artist"),
    
    path('ban_track/<int:track_id>/', views.ban_track, name="ban_track"),
    path('unban_track/<int:track_id>/', views.unban_track, name="unban_track"),
]