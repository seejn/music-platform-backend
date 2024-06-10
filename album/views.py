from django.shortcuts import render
from django.http import JsonResponse
import io, json
from django.utils import timezone
from rest_framework.parsers import JSONParser 
from .serializers import AlbumSerializer, FavouriteAlbumSerializer
from .models import Album, FavouriteAlbum
from Cusers.models import CustomUser,ArtistDetail
from track.models import Music
from utils.fields import check_required_fields
from rest_framework.decorators import api_view,permission_classes
from backend.permission import IsAdmin,IsAdminOrArtist,IsArtist,IsUser,IsAdminOrArtistOrUser,IsUserOrArtist
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.permissions import AllowAny,IsAuthenticated

@api_view(['GET'])
@permission_classes([AllowAny])
def get_album(request, album_id):
    try:
        album = Album.objects.get(pk=album_id)
        serializer = AlbumSerializer(album)
        return JsonResponse({"message": f"Album {album_id}", "data": serializer.data}, status=200)
    except Album.DoesNotExist:
        return JsonResponse({"message": "Album not found"}, status=404)



@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_albums(request):
    all_albums = Album.objects.all()
    serializer = AlbumSerializer(all_albums, many=True)
    return JsonResponse({"message": "All Albums", "data": serializer.data}, status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_artist_albums(request, artist_id):
    artist_albums = Album.objects.filter(artist_id = artist_id)
    
    serializer = AlbumSerializer(artist_albums, many=True)
    return JsonResponse({"message": "All Albums", "data": serializer.data}, status=200)


@api_view(['POST'])
@permission_classes([IsArtist])
def create_album(request):
    if request.method == 'POST':
        try:
            # dict_data = json.loads(request.body)
            dict_data = request.POST.dict()

            artist_id = dict_data.get('artist')
            track_ids = [int(id) for id in dict_data.get('tracks').split(',')]
            image = request.FILES.get("image")
            
            dict_data.pop('artist')
            dict_data.pop('tracks')
            
            artist = CustomUser.objects.get(pk=artist_id)
            print(artist_id)
            print(track_ids)
            print(type(artist))
         
 
            for track_id in track_ids:
                track = Music.objects.get(pk=track_id)
                print(track.artist)
                if track.artist.id != artist.id:
                    return JsonResponse({"message": f"Track ID {track_id} does not belong to the artist"}, status=400)
            print("before creating album")
            print(dict_data)

            new_album = Album.objects.create(**dict_data, artist=artist, image=image)
            print("after creating album")

            new_album.track.add(*track_ids)
            new_album.save()
            
            new_album_data = AlbumSerializer(new_album).data
            
            return JsonResponse({"message": "New Album Added Successfully", "data": new_album_data}, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({"message": "Artist not found"}, status=404)
        except Music.DoesNotExist:
            return JsonResponse({"message": "One or more tracks not found"}, status=404)
        except Exception as e:
            print(e)
            return JsonResponse({"message": str(e)}, status=400)
    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)



@api_view(['PUT'])
@permission_classes([IsArtist])
def update_album(request, album_id):
    dict_data = json.loads(request.body)

    album = Album.objects.get(pk=album_id)
    if request.user.id != album.artist.id:
        raise PermissionDenied("You do not have permission to perform this action.") 
    album.__dict__.update(dict_data)
    album.save()
    album = Album.objects.get(pk=album_id)
    updated_album = AlbumSerializer(album).data
    
    return JsonResponse({"message": "Album Updated Successfully", "data": updated_album}, status=200)
    


@api_view(['DELETE'])
@permission_classes([IsArtist])
def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    if request.user.id != album.artist.id:
        raise PermissionDenied("You do not have permission to perform this action.") 
    album.soft_delete()
    deleted_album = AlbumSerializer(album).data
    return JsonResponse({"message": "Album Deleted Successfully", "data": deleted_album}, status=200)



@api_view(['PUT'])
@permission_classes([IsArtist])
def update_tracks_in_album(request, album_id):
    if request.method == 'PUT':
        try:
            dict_data = json.loads(request.body)
            track_ids = dict_data.get('track', [])

            album = Album.objects.get(pk=album_id)
            artist = album.artist
            if request.user.id != artist.id:
                raise PermissionDenied("You do not have permission to perform this action.") 

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



@api_view(['DELETE'])
@permission_classes([IsArtist])
def delete_tracks_from_album(request, album_id):
    if request.method == 'DELETE':
        try:
            dict_data = json.loads(request.body)
            track_ids = dict_data.get('track', [])

            album = Album.objects.get(pk=album_id)
            artist = album.artist
            if request.user.id != artist.id:
                raise PermissionDenied("You do not have permission to perform this action.") 

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
@api_view(['GET'])
@permission_classes([IsAdminOrArtistOrUser])
def get_all_users_favourite_albums(request):
    all_users_favourite_albums = FavouriteAlbum.objects.all()
    
    if not all_users_favourite_albums:
        return JsonResponse({"message": "No Album Found"}, status=404)  

    all_users_favourite_albums = FavouriteAlbumSerializer(all_users_favourite_albums, many=True).data
    return JsonResponse({"message": "Favourite Albums", "data": all_users_favourite_albums}, status=200)



@api_view(['POST'])
@permission_classes([IsUserOrArtist])
def create_favourite_album(request):

    dict_data = json.loads(request.body)
    user_id = dict_data.get("user_id")
    album_id = dict_data.get("album")

    dict_data.pop("album")
    try:
        favouritealbum = FavouriteAlbum.objects.get(user_id=user_id)
        favouritealbum.album.add(album_id)
        favouritealbum.save()
        favouritealbum = FavouriteAlbumSerializer(favouritealbum)
        return JsonResponse({"message":"new album added","data":favouritealbum.data},status=200)
    except FavouriteAlbum.DoesNotExist:
        pass

    try:
        print(user_id)
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return JsonResponse({"message": "User not Found"}, status=404)  

    print("dict_data", dict_data)
    new_favourite_album = FavouriteAlbum.objects.create(**dict_data)
    try:
        Album.objects.get(pk=album_id)
    except Album.DoesNotExist:
        return JsonResponse({"message": "Album not Available"}, status=404)  

    print(album_id)
    new_favourite_album.album.add(album_id)
    new_favourite_album.save()

    serializer = FavouriteAlbumSerializer(new_favourite_album)

    return JsonResponse({"message": f"create favourite album for user", "data": serializer.data}, status=200)

@api_view(['GET'])
@permission_classes([IsAdminOrArtistOrUser])
def get_user_favourite_album(request, user_id):
    favourite_album = FavouriteAlbum.objects.get(user_id=user_id)
    serializer = FavouriteAlbumSerializer(favourite_album)

    return JsonResponse({"message": f"Favourite Album ", "data": serializer.data}, status=200)    


@api_view(['DELETE'])
@permission_classes([IsUserOrArtist])
def delete_favourite_album(request, favouritealbum_id):
    try:
        favouritealbum = FavouriteAlbum.objects.get(pk=favouritealbum_id)
        if request.user.id != favouritealbum.user.id:
            raise PermissionDenied("You do not have permission to perform this action.") 
    except FavouriteAlbum.DoesNotExist:
        return JsonResponse({"message": "Favourite Album not Found"}, status=404)  

    favouritealbum.soft_delete()

    favouritealbum = FavouriteAlbumSerializer(favouritealbum).data
    return JsonResponse({"message": "Favourite Album deleted successfully", "data": favouritealbum}, status=200)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  
def remove_album_from_favourite_album(request,user_id,album_id):
    favourite_album = FavouriteAlbum.objects.get(user_id=user_id)
    favourite_album.album.remove(album_id)
    favourite_album.save()
    favourite_album=FavouriteAlbumSerializer(favourite_album)
    return JsonResponse({"message":"Remove playlist from favourite playlist","data":favourite_album.data},status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def check_favourite_album(request,user_id,album_id):
    try:
        favourite_album = FavouriteAlbum.objects.get(user_id=user_id)
        favourite_album.album.get(pk=album_id)
        return JsonResponse({"is_favourite":True},status=200)
    except:
        return JsonResponse({"is_favourite":False},status=200)
