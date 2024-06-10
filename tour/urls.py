from django.urls import path
from . import views

urlpatterns = [
    path('get_all_tours/',views.get_all_tours,name="get_all_tours"),
    path("get_artist_tour/<int:artist_id>/",views.get_artist_tour, name="get_artist_tour"),
    path('create/', views.create_tour, name="create_tour"),
    path('update/<int:tour_id>/', views.update_tour, name="update_tour"),
    path('delete/<int:tour_id>/', views.delete_tour, name="delete_tour"),
    path('get_favorite_tour/<int:user_id>/',views.get_user_favorite_playlist_tours, name="user_playlist")
]