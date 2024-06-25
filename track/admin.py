from django.contrib import admin

# Register your models here.
from .models import Music, Playlist, FavouritePlaylist,SharedPlaylist

admin.site.register(Music)
admin.site.register(Playlist)
admin.site.register(FavouritePlaylist)
admin.site.register(SharedPlaylist)
