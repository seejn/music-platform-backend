from django.db import models
from Cusers.models import CustomUser
from django.utils import timezone
from genre.models import Genre
from managers.SoftDelete import SoftDeleteManager
from utils.save_image import save_to_track_media, save_to_playlist_media
from django.core.exceptions import ObjectDoesNotExist

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

    is_banned = models.BooleanField(default=False)
    
    class SoftDeleteAndBannedManager(SoftDeleteManager):

        def get_queryset(self):
            all_tracks = super().get_queryset().filter(is_deleted=False)
            for track in all_tracks:
                if track.is_banned:
                    print("inside get_queryset models.py track")
                    print("ban_until", track.track.banned_until)
                    print("CURR_TIME", time.time())
                if track.is_banned and track.track.banned_until < time.time():
                    track.track.reset_ban_status()
            return all_tracks.filter(is_banned=False)

    objects = SoftDeleteAndBannedManager()

    def __str__(self):
        return f"{self.id} {self.title}"

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


class Playlist(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    track = models.ManyToManyField(Music)
    created_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to=save_to_playlist_media)


    PLAYLIST_TYPES = [
        (0, 'Public'),
        (1, 'Private'),
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
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    
    objects = SoftDeleteManager()

    class Meta:
        db_table = "favourite_playlist"

    def __str__(self):
        return f"{self.id} {self.user.email}"

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

