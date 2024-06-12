from rest_framework import serializers
from .models import RandBTrack, ReportTrack

from Cusers.serializers import CustomUserSerializer
from track.serializers import TrackSerializer

class RandBTrackSerializer(serializers.ModelSerializer):
    track = TrackSerializer(read_only=True)
    class Meta:
        model = RandBTrack
        fields = '__all__'



class ReportTrackSerializer(serializers.ModelSerializer):
    track = TrackSerializer(read_only=True)
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = ReportTrack 
        fields = '__all__'


