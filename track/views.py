from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io, json
# Create your views here.
from django.utils import timezone
from rest_framework.parsers import JSONParser 
from .serializers import TrackSerializer
from .models import Music
from Cusers.models import CustomUser
from genre.models import Genre

def get_track(request, track_id):
    track = Music.objects.get(pk=track_id)
    serializer = TrackSerializer(track)

    return JsonResponse({"message": f"Track {track_id}", "data": serializer.data}, status=200)    

def get_all_tracks(request):
    all_tracks = Music.objects.all()
    serializer = TrackSerializer(all_tracks, many=True)

    return JsonResponse({"message": f"All Tracks", "data": serializer.data}, status=200)    

@csrf_exempt
def create_track(request):
    # stream = io.BytesIO(request.body)
    # dict_data = JSONParser().parse(stream)
    dict_data = json.loads(request.body)
   
    artist_id = dict_data.get('artist')
    genre_id = dict_data.get('genre')
    del dict_data['artist']
    del dict_data['genre']
    
    artist = CustomUser.objects.get(pk=artist_id)
    genre = Genre.objects.get(pk=genre_id)

    new_track = Music.objects.create(**dict_data, artist=artist, genre=genre)
    new_track = TrackSerializer(new_track).data

    return JsonResponse({"message": "New Track Added Successfully", "data": new_track}, status=200)

@csrf_exempt
def update_track(request, track_id):
    dict_data = json.loads(request.body)

    track = Music.objects.get(pk=track_id)
    track.__dict__.update(dict_data)
    track.save()
    track = Music.objects.get(pk=track_id)
    updated_track = TrackSerializer(track).data
    
    return JsonResponse({"message": "Track Updated Successfully", "data": updated_track}, status=200)
    
@csrf_exempt
def delete_track(request, track_id):
    track = Music.objects.get(pk=track_id)
    track.soft_delete()
    track = Music.objects.get(pk=track_id)
    deleted_track = TrackSerializer(track).data

    return JsonResponse({"message": "Track Deleted Successfully", "data": deleted_track}, status=200)
