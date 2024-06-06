from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io, json
from django.utils import timezone
from django.db import IntegrityError
from rest_framework.parsers import JSONParser 
from .serializers import TrackSerializer
from .models import Music, Playlist, FavouritePlaylist
from Cusers.models import CustomUser
from genre.models import Genre
from .serializers import PlayListSerializer, FavouritePlaylistSerializer
from rest_framework.decorators import api_view, permission_classes
from utils.fields import check_required_fields, does_field_exist
from rest_framework.permissions import AllowAny,IsAuthenticated
from backend.permission import IsArtist, IsAdmin,IsAdminOrArtist,IsUser,IsAdminOrArtistOrUser,IsUserOrArtist
from rest_framework.exceptions import PermissionDenied


@api_view(['GET'])
@permission_classes([AllowAny])
def get_artist_track(request, artist_id):
    try:
        artist = CustomUser.objects.get(pk=artist_id)
        
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "Artist not Available"}, status=404)    

    tracks = Music.objects.all().filter(artist_id=artist_id)

    serializer = TrackSerializer(tracks, many=True)

    return JsonResponse({"message": f"Artist {artist_id} Tracks", "data": serializer.data}, status=200)  


@api_view(['GET'])
@permission_classes([AllowAny])
def get_track(request, track_id):
    try:
        track = Music.objects.get(pk=track_id)
        
    except Music.DoesNotExist:
        return JsonResponse({"message": "Track not Available"}, status=404)    

    serializer = TrackSerializer(track)

    return JsonResponse({"message": f"Track {track_id}", "data": serializer.data}, status=200)    



@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_tracks(request):
    all_tracks = Music.objects.all()
    if not all_tracks:
        return JsonResponse({"message": "No track Available"}, status=404)    

    serializer = TrackSerializer(all_tracks, many=True)

    return JsonResponse({"message": f"All Tracks", "data": serializer.data}, status=200)    



@api_view(['POST'])
@permission_classes([IsArtist])
def create_track(request):
    # stream = io.BytesIO(request.body)
    # dict_data = JSONParser().parse(stream)
    # dict_data = json.loads(request.body)

    dict_data = request.POST.dict()
    print(dict_data)
    input_fields = list(dict_data.keys())
    image = request.FILES.get("image")



    required_fields = ["title", "duration", "artist", "genre"]

    if not check_required_fields(input_fields, required_fields):
        return JsonResponse({"message": f"Required Fields: {required_fields}"}, safe=False, status=400)    
   
    artist_id = dict_data.get('artist')
    genre_id = dict_data.get('genre')
    artist = genre = None

    del dict_data['artist']
    try:
        artist = CustomUser.objects.get(pk=artist_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "Artist not Available"}, status=404)    

    if genre_id:
        del dict_data['genre']
        try:
            genre = Genre.objects.get(pk=genre_id)
        except Genre.DoesNotExist:
            return JsonResponse({"message": "Genre not Available"}, status=404)    

    new_track = Music.objects.create(**dict_data, artist=artist, genre=genre, image=image)
    new_track = TrackSerializer(new_track).data

    return JsonResponse({"message": "New Track Added Successfully", "data": new_track}, status=200)





@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_track(request, track_id):
    dict_data = json.loads(request.body)
    input_fields = list(dict_data.keys())
    
    try:
        track = Music.objects.get(pk=track_id)
    except Music.DoesNotExist:
        return JsonResponse({"message": "Track not Available"}, status=404) 

    required_fields = list(track.__dict__.keys())

    print(input_fields)
    print(required_fields)

    if not does_field_exist(input_fields, required_fields):
        return JsonResponse({"message": "Field not Available"}, status=400)  
    
  
    if request.user.id != track.artist.id:
        raise PermissionDenied("You do not have permission to perform this action.")  
    
    track.__dict__.update(dict_data)
    try:
        track.save()
    except IntegrityError:
        return JsonResponse({"message": "Not Available"}, status=404)   

    track = Music.objects.get(pk=track_id)
    updated_track = TrackSerializer(track).data
    
    return JsonResponse({"message": "Track Updated Successfully", "data": updated_track}, status=200)

def does_field_exist(input_fields, required_fields):
    return all(field in required_fields for field in input_fields)

    



@api_view(['DELETE'])
@permission_classes([IsArtist])
def delete_track(request, track_id):
    try:
        track = Music.objects.get(pk=track_id)
    except Music.DoesNotExist:
        return JsonResponse({"message": "Track not Available"}, status=404) 
    if request.user.id != track.artist.id:
        raise PermissionDenied("You do not have permission to perform this action.")  
    track.soft_delete()
    deleted_track = TrackSerializer(track).data

    return JsonResponse({"message": "Track Deleted Successfully", "data": deleted_track}, status=200)



#PLaylist view

@api_view(['GET'])
@permission_classes([AllowAny])
def get_playlist(request, playlist_id):
    playlist = Playlist.objects.get(pk=playlist_id)
    serializer = PlayListSerializer(playlist)

    return JsonResponse({"message": f"Playlist {playlist_id}", "data": serializer.data}, status=200)    



@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_playlists(request):
    all_playlists = Playlist.objects.all()
    serializer = PlayListSerializer(all_playlists, many=True)

    return JsonResponse({"message": f"All Playlists", "data": serializer.data}, status=200)    



@api_view(['POST'])
@permission_classes([IsUserOrArtist])
def create_playlist(request):
    dict_data = request.POST.dict()
    image = request.FILES.get("image")

    user_id = dict_data.get('user')
    track_ids = dict_data.get('track')



    del dict_data['user']
    del dict_data['track']

    user = CustomUser.objects.get(pk=user_id)

    new_playlist = Playlist.objects.create(**dict_data, user=user,image=image)
    
    new_playlist.track.add(*track_ids)
    new_playlist.save()
    
    new_playlist = PlayListSerializer(new_playlist).data

    return JsonResponse({"message": "New Playlist Added Successfully", "data": new_playlist}, status=200)



@api_view(['PUT'])
@permission_classes([IsUserOrArtist])
def update_playlist(request, playlist_id):
    dict_data = json.loads(request.body)

    playlist = Playlist.objects.get(pk=playlist_id)
    if request.user.id != playlist.user.id:
        raise PermissionDenied("You do not have permission to perform this action.") 
    playlist.__dict__.update(dict_data)
    playlist.save()
    playlist = Playlist.objects.get(pk=playlist_id)
    updated_playlist = PlayListSerializer(playlist).data
    
    return JsonResponse({"message": "Playlist Updated Successfully", "data": updated_playlist}, status=200)
    


@api_view(['DELETE'])
@permission_classes([IsUserOrArtist])
def delete_playlist(request, playlist_id):
    playlist = Playlist.objects.get(pk=playlist_id)
    if request.user.id != playlist.user.id:
        raise PermissionDenied("You do not have permission to perform this action.") 
    playlist.soft_delete()
    deleted_playlist = PlayListSerializer(playlist).data
    return JsonResponse({"message": "Playlist Deleted Successfully", "data": deleted_playlist}, status=200)



# favourite playlist


@api_view(['GET'])
@permission_classes([IsAdminOrArtist])
def get_all_users_favourite_playlists(request):
    all_users_favourite_playlists = FavouritePlaylist.objects.all()
    
    if not all_users_favourite_playlists:
        return JsonResponse({"message": "No Favourite Playlists Found"}, status=404)  

    all_users_favourite_playlists = FavouritePlaylistSerializer(all_users_favourite_playlists, many=True).data

    return JsonResponse({"message": "Favourite Playlists", "data": all_users_favourite_playlists}, status=200)



@api_view(['GET'])
@permission_classes([IsAdminOrArtistOrUser])
def get_specific_favourite_playlist(request, favouriteplaylist_id):
    favourit_playlist = FavouritePlaylist.objects.get(pk=favouriteplaylist_id)
    serializer = FavouritePlaylistSerializer(favourit_playlist)

    return JsonResponse({"message": f"Playlist {favouriteplaylist_id}", "data": serializer.data}, status=200)    



@api_view(['POST'])
@permission_classes([IsUserOrArtist])
def create_favourite_playlist(request):

    dict_data = json.loads(request.body)
    user_id = dict_data.get("user_id")
    playlist_id = dict_data.get("playlist")

    del dict_data["playlist"]

    try:
        print(user_id)
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "User not Found"}, status=404)  

    print("dict_data", dict_data)
    new_favourite_playlist = FavouritePlaylist.objects.create(**dict_data)
    try:
        Playlist.objects.get(pk=playlist_id)
    except Playlist.DoesNotExist:
        return JsonResponse({"message": "Playlist not Available"}, status=404)  

    print(playlist_id)
    new_favourite_playlist.playlist.add(playlist_id)
    new_favourite_playlist.save()

    serializer = FavouritePlaylistSerializer(new_favourite_playlist)

    return JsonResponse({"message": f"create favourite playlist for user", "data": serializer.data}, status=200)



@api_view(['DELETE'])
@permission_classes([IsUserOrArtist])
def delete_favourite_playlist(request, favourite_playlist_id):
    try:
        favourite_playlist = FavouritePlaylist.objects.get(pk=favourite_playlist_id)
    except FavouritePlaylist.DoesNotExist:
        return JsonResponse({"message": "Favourite playlist not Found"}, status=404)  
    if request.user.id != favourite_playlist.user.id:
        raise PermissionDenied("You do not have permission to perform this action.") 
    favourite_playlist.soft_delete()

    favourite_playlist = FavouritePlaylistSerializer(favourite_playlist).data
    return JsonResponse({"message": "Favourite playlist deleted successfully", "data": favourite_playlist}, status=200)