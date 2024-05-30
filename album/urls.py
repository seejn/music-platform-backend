from django.urls import path
from . import views

urlpatterns = [
    path('get_all_albums/', views.get_all_albums, name="get_all_albums"),
    path('<int:album_id>/', views.get_album, name="get_album"),
    path('create/', views.create_album, name="create_album"),
    path('update/<int:album_id>/', views.update_album, name="update_album"),
    path('delete/<int:album_id>/', views.delete_album, name="delete_album"),
]
