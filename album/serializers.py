
from rest_framework import serializers
from .models import Album
from Cusers.serializers import ArtistDetailSerializer
from track.serializers import TrackOnlySerializer

class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistDetailSerializer(read_only=True)
    track = TrackOnlySerializer(read_only=True, many=True)
    
    class Meta:
        model = Album
        fields = '__all__'
