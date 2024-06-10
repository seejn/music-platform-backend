from django.contrib import admin
from .models import CustomUser, ArtistDetail
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(ArtistDetail)