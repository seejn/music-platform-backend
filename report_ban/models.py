from django.db import models
from django.utils import timezone

from Cusers.models import CustomUser
from track.models import Music

import time
# Create your models here.
class RandBTrack(models.Model):
    track = models.OneToOneField(Music, on_delete=models.CASCADE, related_name="track")
    banned_until = models.IntegerField(null=True, blank=True)
    banned_at = models.DateTimeField(null=True, blank=True)
    report_count = models.IntegerField(default=0, blank=True)
    
    class Meta:
        db_table = "report_banned_tracks"

    def __str__(self):
        return f"{self.id} {self.track.title}, report_count: {self.report_count}"

    def reset_ban_status(self):
        self.track.is_banned = False
        self.track.save()
        self.delete()
            

class ReportTrack(models.Model):
    track = models.ForeignKey(Music, on_delete=models.CASCADE, related_name="reported")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="report_track")
    reported_at = models.DateTimeField(default=timezone.now)
    description = models.TextField()


    def __str__(self):
        return f"Track {self.track.id}: {self.track.title} reported by user {self.user.id}: {self.user.first_name}_{self.user.last_name}"


class BannedTrack(models.Model):
    track = models.OneToOneField(Music, on_delete=models.CASCADE, related_name="banned")
    banned_at = models.DateTimeField(default=timezone.now)
    banned_until = models.IntegerField()

    def __str__(self):
        banned_until_in_datetime = timezone.datetime.fromtimestamp(self.banned_until)
        return f"Track {self.track.id}: {self.track.title} banned at {self.banned_at} for {banned_until_in_datetime}"
