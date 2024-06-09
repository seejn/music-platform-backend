from django.urls import path
from . import views

urlpatterns = [

    path('get_artist_albums/<int:artist_id>/', views.get_artist_albums, name="get_artist_albums"),
    path('get_all_albums/', views.get_all_albums, name="get_all_albums"),
    path('<int:album_id>/', views.get_album, name="get_album"),
    path('create/', views.create_album, name="create_album"),
    path('update/<int:album_id>/', views.update_album, name="update_album"),
    path('delete/<int:album_id>/', views.delete_album, name="delete_album"),
  
    path('update_tracks_in_album/<int:album_id>/', views.update_tracks_in_album, name="update_tracks_in_album"),
    path('delete_tracks_from_album/<int:album_id>/', views.delete_tracks_from_album, name='delete_tracks_from_album'),
  
    path('favourite_album/get_all/', views.get_all_users_favourite_albums, name="get_all_users_favourite_albums"),
    path('favourite_album/create/', views.create_favourite_album, name="create_favourite_album"),
    path('favourite_album/delete/<int:favouritealbum_id>/', views.delete_favourite_album, name="delete_favourite_album"),
]
