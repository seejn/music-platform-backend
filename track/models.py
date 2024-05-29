from django.db import models
from CustomUser.models import CustomUser
from django.utils import timezone
from genre.models import Genre

class Music(models.Model):
    title = models.CharField(max_length=100)
    duration = models.CharField(max_length=10)
    artist = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    release_date = models.DateField(auto_now_add=True)
    is_deleted=models.BooleanField(default=False)
    cover = models.CharField(default="image.png")  
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.title

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()