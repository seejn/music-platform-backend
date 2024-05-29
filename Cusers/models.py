from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

from Roles.models import Role

# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=50, unique=True)
    image = models.CharField(default="https://via.placeholder.com/150", max_length=50)
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL, related_name="user")
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

    objects = CustomUserManager()

    class Meta:
        db_table = "c_users"

    def __str__(self):
        return self.email