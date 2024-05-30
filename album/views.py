from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io, json
# Create your views here.
from django.utils import timezone
from rest_framework.parsers import JSONParser 
from .serializers import AlbumSerializer
from .models import Album
from Cusers.models import CustomUser


def get_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    serializer = AlbumSerializer(album)

    return JsonResponse({"message": f"Album {album_id}", "data": serializer.data}, status=200)    

def get_all_albums(request):
    all_albums = Album.objects.all()
    serializer = AlbumSerializer(all_albums, many=True)

    return JsonResponse({"message": f"All Albums", "data": serializer.data}, status=200)    

@csrf_exempt
def create_album(request):
    dict_data = json.loads(request.body)
    artist_id = dict_data.get('artist')
    del dict_data['artist']

    
    artist = CustomUser.objects.get(pk=artist_id)


    new_album = Album.objects.create(**dict_data, artist=artist)
    new_album = AlbumSerializer(new_album).data

    return JsonResponse({"message": "New Album Added Successfully", "data": new_album}, status=200)

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
