from django.contrib import admin
from .models import Playlist
# Register your models here.
from .models import Music

admin.site.register(Music)
admin.site.register(Playlist)
