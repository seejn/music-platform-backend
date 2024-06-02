from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io, json
# Create your views here.
from django.utils import timezone
from rest_framework.parsers import JSONParser 
from .serializers import AlbumSerializer
from .models import Album
from Cusers.models import CustomUser,ArtistDetail
from track.models import Music

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
            track_ids = dict_data.get('track')
            
            del dict_data['artist']
            del dict_data['track']
            
            artist = ArtistDetail.objects.get(artist_id=artist_id)
            
 
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
    album = Album.objects.get(pk=album_id)
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