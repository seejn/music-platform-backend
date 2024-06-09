from django.shortcuts import render
from django.utils import timezone
import time, math
# Create your views here.
def report_track(request, track_id):
    try: 
        reported_track = RandBTrack.objects.get(track_id=track_id)
    except RandBTrack.DoesNotExist:
        try:
            track = Music.objects.get(pk=track_id)
            reported_track = RandBTrack.objects.create(track=track)
        except Music.DoesNotExist:
            return JsonResponse({"message": "Track isnot Available"}, status=200)
    
    if reported_track.report_count >= 5:
        CURR_TIME = time.time()
        DEFAULT_BAN_TIME = 60
        DEFALULT_BAN_TIME_IN_HOURS = 60/3600
        
        reported_track.track.is_banned = True
        reported_track.ban_time = math.floor() + DEFAULT_BAN_TIME
        reported_track.banned_at = timezone.now()
        reported_track.save()

        reported_track = RandBTrackSerializer(reported_track)
        return JsonResponse({"message": f"Track Banned for {DEFALULT_BAN_TIME_IN_HOURS}", "data": reported_track.data}, status=200)

    reported_track += 1
    reported_track = RandBTrackSerializer(reported_track)
    return JsonResponse({"message": "Track reported Successfully", "data": reported_track.data}, status=200)
    
