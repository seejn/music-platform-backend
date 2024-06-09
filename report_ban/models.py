from django.db import models
from track.models import Music
import time
# Create your models here.
class RandBTrack(models.Model):
    track = models.OneToOneField(Music, on_delete=models.CASCADE, related_name="track")
    ban_time = models.IntegerField(null=True, blank=True)
    banned_at = models.DateTimeField(null=True, blank=True)
    report_count = models.IntegerField(default=0, blank=True)
    
    class Meta:
        db_table = "report_banned_tracks"

    def __str__(self):
        return f"{self.id} {self.track.title}, report_count: {self.report_count}"

    def reset_ban_status(self):
        if self.ban_time and self.ban_time < time.time():
            self.track.is_banned = False
            self.save()
            self.delete()