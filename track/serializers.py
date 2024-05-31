from rest_framework import serializers
from .models import Music
from .models import Playlist

from Cusers.serializers import ArtistSerializer,CustomUserSerializer
from genre.serializers import GenreSerializer

class TrackSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    genre = GenreSerializer(read_only=True)
    class Meta:
        model = Music
        fields = "__all__"


class TrackOnlySerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    class Meta:
        model = Music
        fields = "__all__"


class PlayListSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only = True)
    track = TrackSerializer(read_only=True,many=True)
    class Meta:
        model = Playlist
        fields = '__all__'