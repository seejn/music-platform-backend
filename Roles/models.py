from django.db import models


class Role(models.Model):
    role = models.CharField(max_length=50) 

    def __str__(self):
        return self.role



