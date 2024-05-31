from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io, json
# Create your views here.
from django.utils import timezone
from django.db import IntegrityError

from rest_framework.parsers import JSONParser 
from .serializers import TrackSerializer
from .models import Music
from Cusers.models import CustomUser
from genre.models import Genre

from utils.fields import check_required_fields, does_field_exist

def get_track(request, track_id):
    try:
        track = Music.objects.get(pk=track_id)
    except Music.DoesNotExist:
        return JsonResponse({"message": "Track not Available"}, status=404)    

    serializer = TrackSerializer(track)

    return JsonResponse({"message": f"Track {track_id}", "data": serializer.data}, status=200)    

def get_all_tracks(request):
    all_tracks = Music.objects.all()
    if not all_tracks:
        return JsonResponse({"message": "No track Available"}, status=404)    

    serializer = TrackSerializer(all_tracks, many=True)

    return JsonResponse({"message": f"All Tracks", "data": serializer.data}, status=200)    

@csrf_exempt
def create_track(request):
    # stream = io.BytesIO(request.body)
    # dict_data = JSONParser().parse(stream)
    dict_data = json.loads(request.body)
    
    input_fields = list(dict_data.keys())
    required_fields = ["title", "duration", "artist"]

    if not check_required_fields(required_fields, input_fields):
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
    

    new_track = Music.objects.create(**dict_data, artist=artist, genre=genre)
    new_track = TrackSerializer(new_track).data

    return JsonResponse({"message": "New Track Added Successfully", "data": new_track}, status=200)

@csrf_exempt
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
        
    track.__dict__.update(dict_data)
    try:
        track.save()
    except IntegrityError:
        return JsonResponse({"message": "Not Available"}, status=404)   

    track = Music.objects.get(pk=track_id)
    updated_track = TrackSerializer(track).data
    
    return JsonResponse({"message": "Track Updated Successfully", "data": updated_track}, status=200)
    
@csrf_exempt
def delete_track(request, track_id):
    try:
        track = Music.objects.get(pk=track_id)
    except Music.DoesNotExist:
        return JsonResponse({"message": "Track not Available"}, status=404) 

    track.soft_delete()
    track = Music.objects.get(pk=track_id)
    deleted_track = TrackSerializer(track).data

    return JsonResponse({"message": "Track Deleted Successfully", "data": deleted_track}, status=200)
