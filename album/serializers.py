
from rest_framework import serializers
from .models import Album, FavouriteAlbum
from Cusers.serializers import ArtistSerializer, CustomUserSerializer
from track.serializers import TrackOnlySerializer


class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only = True)
    track = TrackOnlySerializer(read_only=True,many=True)
    class Meta:
        model = Album
        fields = '__all__'

class FavouriteAlbumSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only = True)
    albums = AlbumSerializer(read_only=True, many=True)
    class Meta:
        model = FavouriteAlbum
        fields = '__all__'
