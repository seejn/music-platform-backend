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
from .decorators import check_expiry_status

from .models import RandBTrack, ReportTrack, BannedTrack
from Cusers.models import CustomUser
from track.models import Music

from . import tasks


from datetime import datetime


import time, math, json


DEFAULT_BAN_TIME_IN_SECONDS = 60
DEFALULT_BAN_TIME_IN_HOURS = 60/3600
# Create y
# our views here.
def ban(track):
    if not track:
        return
    CURR_TIME = time.time()

    return BannedTrack.objects.create(track=track, banned_until=math.floor(CURR_TIME) + DEFAULT_BAN_TIME_IN_SECONDS)


def unban(track):
    BannedTrack.objects.filter(track=track).delete()
    return track







# def report_track(request, track_id):
#     try: 
#         reported_track = RandBTrack.objects.get(track_id=track_id)
#     except RandBTrack.DoesNotExist:
#         try:
#             track = Music.objects.get(pk=track_id)
#             reported_track = RandBTrack.objects.create(track=track)
#         except Music.DoesNotExist:
#             return JsonResponse({"message": "Track is not Available"}, status=200)

#     reported_track.report_count += 1
    
#     if reported_track.report_count >= 5:
#         banned_track = ban(reported_track)

#         banned_track = RandBTrackSerializer(banned_track)
#         return JsonResponse({"message": f"Track Banned for {DEFALULT_BAN_TIME_IN_HOURS} Hours", "data": banned_track.data}, status=200)

#     reported_track.save()

#     reported_track = RandBTrackSerializer(reported_track)
#     return JsonResponse({"message": "Track reported Successfully", "data": reported_track.data}, status=200)
    
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
    except (Music.DoesNotExist, CustomUser.DoesNotExist):
        return JsonResponse({"message": "Something went wrong"}, status=400)    

    if ReportTrack.objects.filter(track=track).count() > 4:
        track = Music.objects.filter(pk=track_id).first()
        ban(track)
        print("before response")
        return JsonResponse({"message": "Track reported Successfully"}, status=200)


    reported_track = ReportTrackSerializer(reported_track)

    return JsonResponse({"message": "Track reported Successfully", "data": reported_track.data}, status=200)















# def get_all_reported_tracks(request):
#     all_reported_tracks = RandBTrack.objects.all()

#     all_reported_tracks = RandBTrackSerializer(all_reported_tracks, many=True)
#     return JsonResponse({"message": "All reported Tracks", "data": all_reported_tracks.data}, status=200)





@check_expiry_status
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









# def get_reported_tracks_of_artist(request, artist_id):
#     reported_tracks = RandBTrack.objects.filter(track__artist_id=artist_id)
#     serialized_tracks = RandBTrackSerializer(reported_tracks, many=True).data
#     return JsonResponse({"message": f"Reported songs of artist: {artist_id}", "data": serialized_tracks}, status=200)






@check_expiry_status
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

    to_remove_report.delete()

    if ReportTrack.objects.filter(track=track).count() < 5:
        unban(track)

    is_banned = BannedTrack.objects.filter(track=track).exists()
    
    response = {
        "id": track.id,
        "title": track.title,
        "is_banned": is_banned
    }

    return JsonResponse({"message": f"Report removed successfully", "data": response}, status=200)



# def get_all_banned_tracks(request):
#     reported_tracks = RandBTrack.objects.all()
#     all_banned_tracks = []
#     for track in reported_tracks:
#         if track.track.is_banned :
#             all_banned_tracks.append(RandBTrackSerializer(track).data)

#     return JsonResponse({"message": f"All banned songs", "data": all_banned_tracks}, status=200)

@check_expiry_status
def get_all_banned_tracks(request):
    banned_tracks = BannedTrack.objects.all()

    response = []

    for banned_track in banned_tracks:
        Music.objects.all()
        track = TrackOnlySerializer(banned_track.track).data
        artist = ArtistSerializer(banned_track.track.artist).data
        track = {
            "track": track,
            "artist": artist,
            "banned_until": datetime.fromtimestamp(banned_track.banned_until)
        }
        response.append(track)

    return JsonResponse({"message": f"All Banned Tracks", "data": response}, status=200)






@check_expiry_status
def get_banned_tracks_of_artist(request, artist_id):
    print(artist_id)
    artist = CustomUser.objects.get(pk=artist_id)
    banned_tracks = BannedTrack.objects.filter(track__artist__id=artist_id)

    response = []

    for banned_track in banned_tracks:
        response.append({
            "track": TrackOnlySerializer(banned_track.track).data,
            "banned_until": banned_track.banned_until,
            "banned_at": banned_track.banned_at,
            "id": banned_track.id
        })

    return JsonResponse({"message": f"Banned songs of artist: {artist_id}", "data": response}, status=200)
    
        
def ban_track(request, track_id):
    
    try:
        track_to_unban = BannedTrack.objects.get(track_id=track_id).track
    except:
        return JsonResponse({"message": f"Something went wrong while banning the track: {track_id}"}, status=500)

    
    banned_track = ban(track_to_ban)
    
    return JsonResponse({"message": f"Track: {track_id} banned successfully"}, status=200)



@api_view(['DELETE'])
@permission_classes([IsAdmin])
def unban_track(request, track_id):
    try:
        track_to_unban = BannedTrack.objects.get(track_id=track_id).track
    except:
        return JsonResponse({"message": f"Something went wrong while unbanning the track: {track_id}"}, status=500)


    track_to_unban.reported.all().delete()
    track_to_unban.unban()    

    return JsonResponse({"message": f"'{track_to_unban.title}' unbanned successfully"}, status=200)
