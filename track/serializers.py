from rest_framework import serializers
from .models import Music
from .models import Playlist, FavouritePlaylist,SharedPlaylist

from Cusers.serializers import ArtistSerializer, ArtistDetailSerializer, CustomUserSerializer
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
    user = CustomUserSerializer(read_only=True)
    track = TrackSerializer(read_only=True, many=True)
    playlist_type = serializers.ChoiceField(choices=Playlist.PLAYLIST_TYPES, default=1)

    class Meta:
        model = Playlist
        fields = '__all__'

class FavouritePlaylistSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only = True)
    playlist = PlayListSerializer(read_only=True, many=True)
    class Meta:
        model = FavouritePlaylist
        fields = '__all__'

class SharedPlaylistSerializer(serializers.ModelSerializer):
    playlist = PlayListSerializer(read_only=True)
    shared_by = CustomUserSerializer(read_only=True)
    shared_with = CustomUserSerializer(read_only=True)

    class Meta:
        model = SharedPlaylist
        fields = '__all__'

