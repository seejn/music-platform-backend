from django.db import models
from Cusers.models import CustomUser
from django.utils import timezone
from genre.models import Genre
from managers.SoftDelete import SoftDeleteManager
from utils.save_image import save_to_track_media, save_to_playlist_media
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime

import time

class Music(models.Model):
    title = models.CharField(max_length=100)
    duration = models.CharField(max_length=10)
    artist = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    released_date = models.DateField(null=True)
    is_deleted=models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True,blank=True)
    image = models.ImageField(upload_to=save_to_track_media, blank=True, null=True)  
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)

    class SoftDeleteAndBannedManager(SoftDeleteManager):

        def get_queryset(self):
            all_tracks = super().get_queryset().filter(is_deleted=False)
            checked_tracks = []

            banned_tracks = all_tracks.filter(banned__isnull=False)
            
            for track in all_tracks:
                if track.id in checked_tracks:
                    continue

                checked_tracks.append(track.id)

                if track not in banned_tracks and track.reported.count() >= 5:
                    print("from manager",track)
                    track.ban()

                elif track in banned_tracks and track.reported.count() < 5:
                    track.unban()
            
            
            expired_banned_tracks = banned_tracks.filter(banned__banned_until__lt=time.time())
            for track in expired_banned_tracks:
                track.reported.all().delete()
                track.unban()


            return all_tracks.filter(banned__isnull=True)

    objects = SoftDeleteAndBannedManager()

    def __str__(self):
        return f"{self.id} {self.title}"

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    # def check_reported_status_to_ban_unban(self):
    #     if self.filter(banned__isnull=False).count() and self.reported.count() < 5:
    #         self.unban()  
    #     elif self.filter(banned_isnull=True).count() and self.reported.count() >= 5:
    #         self.ban()
    #     else:
    #         pass

    def unban(self):
        self.banned.delete()
    
    def ban(self):
        from report_ban.models import BannedTrack
        
        CURR_TIMESTAMP=time.time()
        DEFAULT_BAN_TIME_IN_SECONDS=60
        
        BannedTrack.objects.create(
            track_id=self.id,
            banned_until=CURR_TIMESTAMP+DEFAULT_BAN_TIME_IN_SECONDS
        )


class Playlist(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    track = models.ManyToManyField(Music)
    created_at = models.DateTimeField(default=datetime.now)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to=save_to_playlist_media)


    PLAYLIST_TYPES = [
        ("0", 'Public'),
        ("1", 'Private'),
    ]
    playlist_type = models.CharField(max_length=2, choices=PLAYLIST_TYPES, default=1)

    objects = SoftDeleteManager()

    def __str__(self):
        return f"{self.id} {self.title}"

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

class FavouritePlaylist(models.Model):
    playlist = models.ManyToManyField(Playlist, related_name="favourite_by")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="favourite_playlist")
    created_at = models.DateTimeField(default=datetime.now)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    
    objects = SoftDeleteManager()

    class Meta:
        db_table = "favourite_playlist"

    def __str__(self):
        return f"{self.id} {self.user.email}"

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.save()

class SharedPlaylist(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='shared_with_users')
    shared_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='shared_playlists')
    shared_with = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='shared_with_by')

    def __str__(self):
        return f"{self.playlist.title} shared by {self.shared_by.email} with {self.shared_with.email}"