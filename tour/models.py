from django.db import models
from Cusers.models import CustomUser
from django.utils import timezone
from managers.SoftDelete import SoftDeleteManager

class Tour(models.Model):
    title=models.CharField(max_length=20)
    artist = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    date=models.DateField(default=timezone.now)
    location=models.CharField(max_length=20)
    time = models.TimeField(default=timezone.now)
    venue=models.CharField(max_length=20)
    is_deleted=models.BooleanField(default=False)
    deleted_at=models.DateTimeField(null=True,blank=True)

    objects = SoftDeleteManager()

    class Meta:
        db_table = "tour"
    
    def __str__(self):
        return f"{self.id} {self.title}"
    
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


