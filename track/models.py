from django.db import models
from Cusers.models import CustomUser
from django.utils import timezone
from genre.models import Genre

class Music(models.Model):
    title = models.CharField(max_length=100)
    duration = models.CharField(max_length=10)
    artist = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    release_date = models.DateField(null=True)
    is_deleted=models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True,blank=True)
    image = models.CharField(max_length=100,default="image.png")  
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return self.title

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

class Playlist(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    track = models.ManyToManyField(Music)
    created_at = models.DateTimeField(default=timezone.now)
    is_deleted=models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True,blank=True)
    image = models.CharField(max_length=100,default="image.png")  


    def __str__(self):
        return self.title

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

    class Meta:
        db_table = "favourite_playlist"

    def __str__(self):
        return f"{self.id} {self.album.title}"

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

