from django.db import models
from Cusers.models import CustomUser,ArtistDetail
from django.utils import timezone
from track.models import Music
from managers.SoftDelete import SoftDeleteManager

from utils.save_image import save_to_album_media


class Album(models.Model):
    title= models.CharField(max_length=20,unique=True)
    artist=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    track=models.ManyToManyField(Music)
    released_date=models.DateField(null=True)
    image=models.ImageField(null=True, blank=True, upload_to=save_to_album_media)
    is_deleted= models.BooleanField(default=False)
    deleted_at=models.DateTimeField(null=True,blank=True)

    objects = SoftDeleteManager()

    class Meta:
        db_table = "album"

    def __str__(self):
        return f"{self.id} {self.title}"
    
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


class FavouriteAlbum(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="favourite_album")
    album = models.ManyToManyField(Album, related_name="favourite_by")
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()

    class Meta:
        db_table = "favourite_album"

    def __str__(self):
        return f"{self.id} {self.user.email}"

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()