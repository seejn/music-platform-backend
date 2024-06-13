from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Case, When, BooleanField, F
from backend.permission import IsArtist, IsAdmin,IsAdminOrArtist,IsUser,IsAdminOrArtistOrUser,IsUserOrArtist

from rest_framework.decorators import api_view, permission_classes


from track.serializers import TrackOnlySerializer
from Cusers.serializers import CustomUserSerializer, ArtistSerializer
from .serializers import RandBTrackSerializer, ReportTrackSerializer

from .models import RandBTrack, ReportTrack, BannedTrack
from Cusers.models import CustomUser
from track.models import Music

from . import tasks


from datetime import datetime


import time, math, json







@api_view(['POST'])
@permission_classes([IsAdminOrArtistOrUser])
def report_track(request, track_id, user_id):

    if ReportTrack.objects.filter(user_id=user_id, track_id=track_id).exists():
        return JsonResponse({"message": "Your complain has already been submitted"}, status=400)

    if bool(request.body):
        dict_data = json.loads(request.body)
        reason_to_report = dict_data.get("reason")
    

    try:
        track = Music.objects.get(pk=track_id)
        user = CustomUser.objects.get(pk=user_id)
        reported_track = ReportTrack.objects.create(track=track, user=user, description=reason_to_report)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Something went wrong"}, status=200)    


    reported_track = ReportTrackSerializer(reported_track)

    return JsonResponse({"message": "Track reported Successfully", "data": reported_track.data}, status=200)













def get_all_reported_tracks(request):
    all_reported_tracks_summary = ReportTrack.objects.values(
        'track__id',
        'track__title',
        artist_first_name=F('track__artist__first_name'),
        artist_last_name=F('track__artist__last_name')
    ).annotate(
        report_count=Count('track'),
        is_banned=Case(
            When(track__banned__isnull=False, then=True),
            default=False,
            output_field=BooleanField()
        )
    )


    return JsonResponse({"message": "All reported Tracks", "data": list(all_reported_tracks_summary)}, status=200)














def get_reported_track(request, track_id):
    reported_track = ReportTrack.objects.filter(track_id = track_id)
    track = reported_track.first().track
    artist = track.artist
    serialized_reported_track = []

    serialized_track = TrackOnlySerializer(track).data
    artist = ArtistSerializer(artist).data
    is_banned = BannedTrack.objects.filter(track_id=track_id).exists()
    for track in reported_track:
        serialized_reported_by = CustomUserSerializer(track.user).data
        dictionary = {
            "id": track.id,
            "reported_by": serialized_reported_by,
            "reported_at": track.reported_at,
            "description": track.description,
        }
        serialized_reported_track.append(dictionary)


    return JsonResponse({"message": f"Reported Track","is_banned": is_banned,"artist": artist, "track": serialized_track, "data": serialized_reported_track}, status=200)




















@api_view(['DELETE'])
@permission_classes([IsAdmin])
def remove_reported_track(request, report_id):
    to_remove_report = ReportTrack.objects.get(pk=report_id)
    track = to_remove_report.track
    track_id = track.id

    to_remove_report.delete()

    track = Music.objects.get(pk=track_id)

    is_banned = BannedTrack.objects.filter(track=track).count() > 0
    
    response = {
        "id": track.id,
        "title": track.title,
        "is_banned": is_banned
    }

    return JsonResponse({"message": f"Reported removed successfully", "data": response}, status=200)











def get_all_banned_tracks(request):
    banned_tracks = BannedTrack.objects.all()

    tracks = []

    for banned_track in banned_tracks:
        track = TrackOnlySerializer(banned_track.track).data
        artist = ArtistSerializer(banned_track.track.artist).data
        track = {
            "track": track,
            "artist": artist,
            "banned_until": datetime.fromtimestamp(banned_track.banned_until)
        }
        tracks.append(track)

    return JsonResponse({"message": f"All Banned Tracks", "data": tracks}, status=200)













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
        try:
            track_to_ban = RandBTrack.objects.create(track_id=track_id)
        except: 
            return JsonResponse({"message": f"Something went wrong while banning the track: {track_id}"}, status=500)
    
    banned_track = ban(track_to_ban)
    banned_track = RandBTrackSerializer(banned_track)
    return JsonResponse({"message": f"Track: {track_id} banned successfully", "data": banned_track.data}, status=200)















@api_view(['DELETE'])
@permission_classes([IsAdmin])
def unban_track(request, track_id):
    try:
        track_to_unban = BannedTrack.objects.get(track_id=track_id).track
    except:
        return JsonResponse({"message": f"Something went wrong while unbanning the track: {track_id}"}, status=500)


    track_to_unban.reported.all().delete()
    track_to_unban.unban()    

    return JsonResponse({"message": f"Track: {track_id} unbanned successfully"}, status=200)
