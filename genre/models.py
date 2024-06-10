from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=20,unique=True)

    class Meta:
        db_table = "genre"

    def __str__(self):
        return self.name