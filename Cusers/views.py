from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from backend.permission import IsAdmin,IsAdminOrArtist,IsArtist,IsUser,IsAdminOrArtistOrUser
import json
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Follow
from track.models import Playlist
from backend.permission import IsAdmin, IsUserOrArtist
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_users(request):
    all_users = CustomUser.objects.all()
    serializer = CustomUserSerializer(all_users, many=True)

    return JsonResponse({"message": f"All Users", "data": serializer.data}, status=200) 



@api_view(['GET'])
@permission_classes([AllowAny])
def get_user(request, user_id):
    user= CustomUser.objects.get(pk=user_id)
    serializer = CustomUserSerializer(user)

    return JsonResponse({"message": f"User {user_id}", "data": serializer.data}, status=200) 





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, pk=user_id)
    followed_by = request.user

    if followed_by == user_to_follow:
        return JsonResponse({"message": "You cannot follow yourself"}, status=400)

    follow_instance, created = Follow.objects.get_or_create(followed_by=followed_by, followed_to=user_to_follow)

    if created:
        return JsonResponse({"message": f"You are now following {user_to_follow.email}"}, status=201)
    else:
        return JsonResponse({"message": f"You are already following {user_to_follow.email}"}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    followed_user = get_object_or_404(CustomUser, id=user_id)
    follow = Follow.objects.filter(followed_by=request.user, followed_to=followed_user)

    if follow.exists():
        follow.delete()
        return JsonResponse({"message": f"You have unfollowed {followed_user.first_name} {followed_user.last_name}."}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"message": f"You are not following {followed_user.first_name} {followed_user.last_name}."}, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_followed_users(request):
    followed_by = request.user  


    follow_relationships = Follow.objects.filter(followed_by=followed_by)
    print(follow_relationships)
    followed_users = [follow.followed_to for follow in follow_relationships]

    serializer = CustomUserSerializer(followed_users, many=True)
    
    return JsonResponse({"message": "Followed Users", "data": serializer.data}, status=200)




def is_following(request, followed_by_id, followed_to_id):
    followed_by = CustomUser.objects.get(pk=followed_by_id)
    is_following_boolean = followed_by.follow.filter(followed_to=followed_to_id).count() > 0

    return JsonResponse({"is_following": is_following_boolean}, status=200)



from track.models import Playlist, SharedPlaylist

from track.serializers import PlayListSerializer
@api_view(['POST'])
@permission_classes([IsAdminOrArtistOrUser])
def share_playlist(request, playlist_id, user_id):
    try:
        playlist = get_object_or_404(Playlist, id=playlist_id)
        user_to_share_with = get_object_or_404(CustomUser, id=user_id)
        current_user = request.user

        if not Follow.objects.filter(followed_by=current_user, followed_to=user_to_share_with).exists():
            return JsonResponse({"message": "You can only share with users you follow"}, status=403)

        shared_playlist = SharedPlaylist.objects.create(playlist=playlist, shared_by=current_user, shared_with=user_to_share_with)

        return JsonResponse({"message": "Playlist shared successfully"}, status=200)
    
    except Playlist.DoesNotExist:
        return JsonResponse({"message": "Playlist not found"}, status=404)
    
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "User not found"}, status=404)





from track.serializers import PlayListSerializer, SharedPlaylistSerializer

@api_view(['GET'])
@permission_classes([IsAdminOrArtistOrUser])
def get_shared_playlists(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)

        shared_playlists = SharedPlaylist.objects.filter(shared_with=user)
        serialized_playlists = SharedPlaylistSerializer(shared_playlists, many=True).data

        return JsonResponse(serialized_playlists, status=200, safe=False)
    
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "User not found"}, status=404)
    
    except Exception as e:

        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error fetching shared playlists for user_id {user_id}: {e}")
        
        return JsonResponse({"message": "Internal Server Error"}, status=500)




