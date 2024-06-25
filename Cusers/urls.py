from django.urls import path
from .views import get_all_users,get_user,follow_user,unfollow_user,get_followed_users,share_playlist,get_shared_playlists,is_following,get_specific_shared_playlist

urlpatterns = [
    path('get_all_users/', get_all_users, name="get_all_users"),
    path('<int:user_id>/', get_user, name="get_user"),
    path('follow/<int:user_id>/', follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow-user'),
    path('all_followed_user/', get_followed_users, name='get_followed_users'),
    path('share-playlist/<int:playlist_id>/user/<int:user_id>/', share_playlist, name='share-playlist'),
    path('get_share_playlist/<int:user_id>/', get_shared_playlists, name='get_shared_playlists'),
    path('is_following/followed_by/<int:followed_by_id>/followed_to/<int:followed_to_id>/', is_following,name='is_following' ),
    path('get_specific_shared_playlist/playlist/<int:playlist_id>/user/<int:user_id>/', get_specific_shared_playlist, name='get_specific_share-playlist'),
]

