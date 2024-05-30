from django.db import models
from Cusers.models import CustomUser
from django.utils import timezone
from track.models import Music
class Album(models.Model):
    title= models.CharField(max_length=20,unique=True)
    artist=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    track=models.ManyToManyField(Music)
    released_date=models.DateField(null=True)
    image=models.CharField(max_length=200,default="image.png")
    is_deleted= models.BooleanField(default=False)
    deleted_at=models.DateTimeField(null=True)

    class Meta:
        db_table = "album"

    def __str__(self):
        return "album"
    
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()