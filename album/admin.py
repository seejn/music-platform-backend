from django.contrib import admin

# Register your models here.
from .models import Album, FavouriteAlbum

admin.site.register(Album)
admin.site.register(FavouriteAlbum)
