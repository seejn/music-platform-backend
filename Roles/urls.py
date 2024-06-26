from django.urls import path
from .views import get_all_artist,get_current_artist,create_user,create_artist,update_user,update_personal_artist_info,login,logout,get_current_user,get_all_userrr,update_user_profile_image,update_artist_profile_image

urlpatterns = [
    path('artists/', get_all_artist, name='get_all_artist'),
    path('users/', get_all_userrr, name='get_all_artist'),
    path('artist/<int:artist_id>/', get_current_artist, name='current_artist_detail'),
    path('user/<int:user_id>/',get_current_user,name='current_user_detail'),
    path('create/', create_user, name="create_user"),
    path('create_artist/', create_artist, name="create_user"),
    path('update_user/<int:user_id>/', update_user, name="update_user"),
    path('update_user_profile_image/<int:user_id>/', update_user_profile_image, name="update_user_profile_image"),
    path('update_artist_profile_image/<int:artist_id>/',update_artist_profile_image, name="update_artist_profile_image"),
    path('artist_personal_info/<int:artist_id>/',update_personal_artist_info, name="update_artist"),
    path('artist_info/<int:artist_id>/',update_user, name="update_artist"),
    # path('update_artist/<int:artist_id>/', update_artist_info, name="update_artist"),
    path('login/',login,name="login"),
    path('logout/',logout,name="logout"),
]

