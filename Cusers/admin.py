from django.contrib import admin
from .models import CustomUser, ArtistDetail, Follow
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(ArtistDetail)
admin.site.register(Follow)