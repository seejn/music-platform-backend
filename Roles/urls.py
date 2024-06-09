from django.urls import path
from .views import get_all_artist,get_current_artist,create_user,create_artist,update_user,update_personal_artist_info,login,logout,get_current_user
urlpatterns = [
    path('artists/', get_all_artist, name='get_all_artist'),
    path('artist/<int:artist_id>/', get_current_artist, name='current_artist_detail'),
    path('user/<int:user_id>/',get_current_user,name='current_user_detail'),
    path('create/', create_user, name="create_user"),
    path('create_artist/', create_artist, name="create_user"),
    path('update_user/<int:user_id>/', update_user, name="update_user"),
    path('artist_personal_info/<int:artist_id>/',update_personal_artist_info, name="update_artist"),
    # path('update_artist/<int:artist_id>/', update_artist_info, name="update_artist"),
    path('login/',login,name="login"),
    path('logout/',logout,name="logout"),
]

