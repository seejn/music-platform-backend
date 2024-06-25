from report_ban.models import BannedTrack
import time



def check_expiry_status(func):
    def wrapper(*args, **kwargs):
        expired_banned_tracks = BannedTrack.objects.filter(banned_until__lt=time.time())
        
        for track in expired_banned_tracks:
            track.track.reported.all().delete()
            track.delete()
        
        return func(*args, **kwargs)
    return wrapper