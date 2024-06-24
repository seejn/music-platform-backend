from django.urls import path
from . import views

urlpatterns = [

    path('get_artist_track/<int:artist_id>/', views.get_artist_track, name="get_artist_track"),
    path('get_all_tracks/', views.get_all_tracks, name="get_all_tracks"),
    path('<int:track_id>/', views.get_track, name="get_track"),
    path('create/', views.create_track, name="create_track"),
    path('update/<int:track_id>/', views.update_track, name="update_track"),
    path('delete/<int:track_id>/', views.delete_track, name="delete_track"),
    
    path('get_user_playlists/<int:user_id>/', views.get_user_playlists, name="get_user_playlists"),
    path('get_all_playlist/', views.get_all_playlists, name="get_all_playlists"),
    path('playlist/<int:playlist_id>/', views.get_playlist, name="get_playlist"),
    path('create_playlist/', views.create_playlist, name="create_playlist"),
    path('update_playlist/<int:playlist_id>/', views.update_playlist, name="update_playlist"),
    path('update_playlist_image/<int:playlist_id>/', views.update_playlist_image, name="update_playlist_image"),
    path('update_privacy_playlist/<int:playlist_id>/', views.update_privacy_playlist, name="update_privacy_playlist"),
    path('add_remove_track_to_playlist/<int:playlist_id>/', views.add_remove_track_to_playlist, name="add_remove_track_to_playlist"),
    path('add_track_to_playlist/<int:playlist_id>/', views.add_track_to_playlist, name="add_remove_track_to_playlist"),
    path('delete_playlist/<int:playlist_id>/', views.delete_playlist, name="delete_playlist"),

    path('favourite_playlist/get_all/', views.get_all_users_favourite_playlists, name="get_all_users_favourite_playlists"),
    path('specific_favourite_playlist/<int:favouriteplaylist_id>/', views.get_specific_favourite_playlist, name="get_specific_favourite_playlists"),
    path('user_favourite_playlist/<int:user_id>/', views.get_user_favourite_playlist, name="get_user_favourite_playlists"),
    path('favourite_playlist/create/', views.create_favourite_playlist, name="create_favourite_playlist"),
    path('favourite_playlist/delete/<int:playlist_id>/', views.delete_favourite_playlist, name="delete_favourite_playlist"),
    path('remove_playlist_from_favourite_playlist/user/<int:user_id>/playlist/<int:playlist_id>/', views.remove_playlist_from_favourite_playlist, name="remove_playlist_from_favourite_playlist"),
    path('check_favourite_playlist/user/<int:user_id>/playlist/<int:playlist_id>/', views.check_favourite_playlist, name="check_favourite_playlist"),
  
]