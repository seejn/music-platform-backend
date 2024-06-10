from rest_framework import serializers
from .models import Tour
from Cusers.serializers import ArtistSerializer,CustomUserSerializer
from track.serializers import FavouritePlaylistSerializer,TrackSerializer


class TourSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    favourite_playlist = FavouritePlaylistSerializer(read_only=True)
    track = TrackSerializer(read_only=True, many=True)
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = Tour
        fields = "__all__"