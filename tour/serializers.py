from rest_framework import serializers
from .models import Tour
from Cusers.serializers import ArtistSerializer


class TourSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    class Meta:
        model = Tour
        fields = "__all__"