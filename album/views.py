from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io, json
# Create your views here.
from django.utils import timezone
from rest_framework.parsers import JSONParser 

from .serializers import AlbumSerializer, FavouriteAlbumSerializer
from .models import Album, FavouriteAlbum
from Cusers.models import CustomUser,ArtistDetail

from track.models import Music

from utils.fields import check_required_fields

@csrf_exempt
def get_album(request, album_id):
    try:
        album = Album.objects.get(pk=album_id)
        serializer = AlbumSerializer(album)
        return JsonResponse({"message": f"Album {album_id}", "data": serializer.data}, status=200)
    except Album.DoesNotExist:
        return JsonResponse({"message": "Album not found"}, status=404)

@csrf_exempt
def get_all_albums(request):
    all_albums = Album.objects.all()
    serializer = AlbumSerializer(all_albums, many=True)
    return JsonResponse({"message": "All Albums", "data": serializer.data}, status=200)


@csrf_exempt
def create_album(request):
    if request.method == 'POST':
        try:
            dict_data = json.loads(request.body)
            
            artist_id = dict_data.get('artist')
            track_ids = dict_data.get('tracks')
            
            del dict_data['artist']
            del dict_data['tracks']
            
            artist = CustomUser.objects.get(pk=artist_id)
 
            for track_id in track_ids:
                track = Music.objects.get(pk=track_id)
                if track.artist.id != artist.id:
                    return JsonResponse({"message": f"Track ID {track_id} does not belong to the artist"}, status=400)
            
            new_album = Album.objects.create(**dict_data, artist=artist)
            new_album.track.add(*track_ids)
            new_album.save()
            
            new_album_data = AlbumSerializer(new_album).data
            
            return JsonResponse({"message": "New Album Added Successfully", "data": new_album_data}, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({"message": "Artist not found"}, status=404)
        except Music.DoesNotExist:
            return JsonResponse({"message": "One or more tracks not found"}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)


@csrf_exempt
def update_album(request, album_id):
    dict_data = json.loads(request.body)

    album = Album.objects.get(pk=album_id)
    
    album.__dict__.update(dict_data)
    album.save()
    album = Album.objects.get(pk=album_id)
    updated_album = AlbumSerializer(album).data
    
    return JsonResponse({"message": "Album Updated Successfully", "data": updated_album}, status=200)
    
@csrf_exempt
def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.soft_delete()
    deleted_album = AlbumSerializer(album).data
    return JsonResponse({"message": "Album Deleted Successfully", "data": deleted_album}, status=200)



@csrf_exempt
def update_tracks_in_album(request, album_id):
    if request.method == 'PUT':
        try:
            dict_data = json.loads(request.body)
            track_ids = dict_data.get('track', [])

            album = Album.objects.get(pk=album_id)
            artist = album.artist

            for track_id in track_ids:
                track = Music.objects.get(pk=track_id)
                if track.artist.id != artist.id:
                    return JsonResponse({"message": f"Track ID {track_id} does not belong to the artist of the album"}, status=400)

            album.track.set(track_ids)
            album.save()

            updated_album = AlbumSerializer(album).data
            return JsonResponse({"message": "Tracks Updated Successfully", "data": updated_album}, status=200)
        except Album.DoesNotExist:
            return JsonResponse({"message": "Album not found"}, status=404)
        except Music.DoesNotExist:
            return JsonResponse({"message": "Tracks not found"}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)

@csrf_exempt
def delete_tracks_from_album(request, album_id):
    if request.method == 'DELETE':
        try:
            dict_data = json.loads(request.body)
            track_ids = dict_data.get('track', [])

            album = Album.objects.get(pk=album_id)
            artist = album.artist

            for track_id in track_ids:
                track = Music.objects.get(pk=track_id)
                if track.artist.id != artist.id:
                    return JsonResponse({"message": f"Track ID {track_id} does not belong to the artist of the album"}, status=400)

            album.track.remove(*track_ids)
            album.save()

            updated_album = AlbumSerializer(album).data
            return JsonResponse({"message": "Tracks Deleted Successfully", "data": updated_album}, status=200)
        except Album.DoesNotExist:
            return JsonResponse({"message": "Album not found"}, status=404)
        except Music.DoesNotExist:
            return JsonResponse({"message": "Tracks not found"}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)
# Favourite Albums

def get_all_users_favourite_albums(request):
    all_users_favourite_albums = FavouriteAlbum.objects.all()
    
    if not all_users_favourite_albums:
        return JsonResponse({"message": "No Album Found"}, status=404)  

    all_users_favourite_albums = FavouriteAlbumSerializer(all_users_favourite_albums, many=True).data

    return JsonResponse({"message": "Favourite Albums", "data": all_users_favourite_albums}, status=200)


@csrf_exempt
def create_favourite_album(request):

    dict_data = json.loads(request.body)
    user_id = dict_data.get("user_id")
    album_ids = dict_data.get("albums")

    del dict_data["albums"]

    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "User not Found"}, status=404)  

    new_favourite_album = FavouriteAlbum.objects.create(**dict_data)

    for album_id in album_ids:
        try:
            Album.objects.get(pk=album_id)
        except Album.DoesNotExist:
            return JsonResponse({"message": "Album not Available"}, status=404)  

    print(album_ids)
    new_favourite_album.albums.set(album_ids)
    new_favourite_album.save()

    serializer = FavouriteAlbumSerializer(new_favourite_album)

    return JsonResponse({"message": f"create favourite album for user", "data": serializer.data}, status=200)

@csrf_exempt
def delete_favourite_album(request, favourite_album_id):
    try:
        favourite_album = FavouriteAlbum.objects.get(pk=favourite_album_id)
    except FavouriteAlbum.DoesNotExist:
        return JsonResponse({"message": "Favourite Album not Found"}, status=404)  

    favourite_album.soft_delete()

    favourite_album = FavouriteAlbumSerializer(favourite_album).data
    return JsonResponse({"message": "Favourite Album deleted successfully", "data": favourite_album}, status=200)
