from rest_framework import serializers
from .models import Music

from Cusers.serializers import ArtistSerializer
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