from django.db import models
from Cusers.models import CustomUser

class Album(models.Model):
    title= models.CharField(max_length=20,unique=True)
    artist=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    released_date=models.DateField(null=True)
    image=models.CharField(max_length=200,default="image.png")

    class Meta:
        db_table = "album"

    def __str__(self):
        return "album"