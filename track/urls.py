from django.urls import path
from . import views

urlpatterns = [
    path('get_all_tracks/', views.get_all_tracks, name="get_all_tracks"),
    path('<int:track_id>/', views.get_track, name="get_track"),
    path('create/', views.create_track, name="create_track"),
    path('update/<int:track_id>/', views.update_track, name="update_track"),
    path('delete/<int:track_id>/', views.delete_track, name="delete_track"),
]