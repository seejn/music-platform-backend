
from rest_framework import serializers
from .models import Album
from Cusers.serializers import ArtistSerializer
from track.serializers import TrackOnlySerializer


class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only = True)
    track = TrackOnlySerializer(read_only=True,many=True)
    class Meta:
        model = Album
        fields = '__all__'
