from rest_framework import serializers
from .models import RandBTrack

from track.serializers import TrackSerializer

class RandBTrackSerializer(serializers.ModelSerializer):
    track = TrackSerializer(read_only=True)
    class Meta:
        model = RandBTrack
        fields = '__all__'
