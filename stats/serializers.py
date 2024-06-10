from rest_framework import serializers
from Cusers.models import CustomUser
from track.models import Music,Playlist
from album.models import Album
class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'dob', 'gender']

class ArtistStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'details']

class TrackStatsSerializer(serializers.ModelSerializer):
    artist = UserStatsSerializer(read_only=True)
    class Meta:
        model = Music
        fields = ['id', 'title', 'artist', 'genre', 'is_banned']

class AlbumStatsSerializer(serializers.ModelSerializer):
    artist = ArtistStatsSerializer(read_only=True)
    tracks = TrackStatsSerializer(source='track', many=True, read_only=True)
    class Meta:
        model = Album
        fields = ['id', 'title', 'artist', 'tracks']

class PlaylistStatsSerializer(serializers.ModelSerializer):
    user = UserStatsSerializer(read_only=True)
    tracks = TrackStatsSerializer(source='track', many=True, read_only=True)
    class Meta:
        model = Playlist
        fields = ['id', 'title', 'user', 'tracks']
