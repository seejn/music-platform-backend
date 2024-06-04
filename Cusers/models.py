
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from Roles.models import Role
from backend.settings import SIMPLE_JWT
from datetime import timedelta
from django.utils import timezone

class ArtistDetail(models.Model):
    stagename = models.CharField(null=True, unique=True, max_length=50)
    biography = models.TextField(null=True, blank=True, max_length=250)
    
    nationality = models.CharField(null=True, blank=True, max_length=50)
    twitter_link = models.CharField(null=True, blank=True, max_length=100)
    facebook_link = models.CharField(null=True, blank=True, max_length=100)
    instagram_link = models.CharField(null=True, blank=True, max_length=100)
 

    def __str__(self):
        return f"Detail: {self.stagename}"
    
    def soft_delete(self):
        self.is_deleted = True
        self.save()


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=50, unique=True)
    image = models.CharField(default="https://via.placeholder.com/150", max_length=50)
    dob = models.DateField(null=True)
    gender = models.CharField( default="male",max_length=10)
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL, related_name="user")
    deleted_at=models.DateTimeField(null=True,blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    details = models.OneToOneField(ArtistDetail, on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = "c_users"

    def __str__(self):
        return f"[{self.id}: {self.email}]"
    
    def soft_delete(self):
        self.is_deleted = True
        self.save()




class Token(models.Model):
    refresh_token = models.CharField(max_length=500)
    access_token = models.CharField(max_length=500)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(default=timezone.now() + SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])

    class Meta:
        unique_together = ('refresh_token', 'user')

