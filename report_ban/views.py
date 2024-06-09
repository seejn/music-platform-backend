from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from .serializers import RandBTrackSerializer
from .models import RandBTrack
from track.models import Music
import time, math

# Create your views here.
def ban(track):
    CURR_TIME = time.time()
    DEFAULT_BAN_TIME = 60
    DEFALULT_BAN_TIME_IN_HOURS = 60/3600
    
    track.track.is_banned = True
    track.ban_time = math.floor(CURR_TIME) + DEFAULT_BAN_TIME
    track.banned_at = timezone.now()
    track.track.save()
    track.save()
    return track


def unban(track):
    track.track.is_banned = False
    track.ban_time = None
    track.banned_at = None
    track.report_count = 0
    track.track.save()
    track.save()
    return track

def report_track(request, track_id):
    try: 
        reported_track = RandBTrack.objects.get(track_id=track_id)
    except RandBTrack.DoesNotExist:
        try:
            track = Music.objects.get(pk=track_id)
            reported_track = RandBTrack.objects.create(track=track)
        except Music.DoesNotExist:
            return JsonResponse({"message": "Track is not Available"}, status=200)
    
    if reported_track.report_count >= 5:
        banned_track = ban_track(reported_track)

        banned_track = RandBTrackSerializer(banned_track)
        return JsonResponse({"message": f"Track Banned for {DEFALULT_BAN_TIME_IN_HOURS} Hours", "data": banned_track.data}, status=200)

    reported_track.report_count += 1
    reported_track.save()

    reported_track = RandBTrackSerializer(reported_track)
    return JsonResponse({"message": "Track reported Successfully", "data": reported_track.data}, status=200)
    


def get_all_reported_tracks(request):
    all_reported_tracks = RandBTrack.objects.all()

    all_reported_tracks = RandBTrackSerializer(all_reported_tracks, many=True)
    return JsonResponse({"message": "All reported Tracks", "data": all_reported_tracks.data}, status=200)



def get_reported_tracks_of_artist(request, artist_id):
    all_reported_tracks = RandBTrack.objects.all()    

    reported_tracks_of_artist = []

    for reported_track in all_reported_tracks:
        if reported_track.track.artist.id == artist_id:
            reported_tracks_of_artist.append(RandBTrackSerializer(reported_track))

    return JsonResponse({"message": f"Reported songs of artist: {artist_id}", "data": reported_tracks_of_artist}, status=200)



def get_all_banned_tracks(request):
    reported_tracks = RandBTrack.objects.all()
    all_banned_tracks = []
    for track in reported_tracks:
        if track.report_count >= 5:
            all_banned_tracks.append(RandBTrackSerializer(track))

    return JsonResponse({"message": f"All banned songs", "data": all_banned_tracks.data}, status=200)



def get_banned_tracks_of_artist(request, artist_id):
    reported_tracks = RandBTrack.objects.all()
    banned_tracks_of_artist = []
    for track in reported_tracks:
        if track.report_count >= 5 and track.track.artist.id == artist_id:
            banned_tracks_of_artist.append(RandBTrackSerializer(track))

    return JsonResponse({"message": f"Banned songs of artist: {artist_id}", "data": banned_tracks_of_artist}, status=200)
    
        
def ban_track(request, track_id):
    try:
        track_to_ban = RandBTrack.objects.get(track_id=track_id)
    except: 
        return JsonResponse({"message": f"Something went wrong while banning the track: {track_id}"}, status=500)
    
    banned_track = ban(track_to_ban)
    banned_track = RandBTrackSerializer(banned_track)
    return JsonResponse({"message": f"Track: {track_id} banned successfully", "data": banned_track.data}, status=200)


def unban_track(request, track_id):
     try:
        track_to_unban = RandBTrack.objects.get(track_id=track_id)
    except: 
        return JsonResponse({"message": f"Something went wrong while unbanning the track: {track_id}"}, status=500)
    
    unbanned_track = unban(track_to_unban)
    unbanned_track = RandBTrackSerializer(unbanned_track)

    return JsonResponse({"message": f"Track: {track_id} unbanned successfully", "data": unbanned_track.data}, status=200)
